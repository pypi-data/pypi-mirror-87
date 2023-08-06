import os
from shutil import copy2
from subprocess import call
from collections import namedtuple
try:
    import numpy as np
except ImportError:
    np = None
try:
    import matplotlib.pyplot as plt
except ImportError:
    plt = None
try:
    import seaborn as sns
except ImportError:
    sns = None


def postprocessor(script):
    """
    This is the key function that controls composition
    of the previously rendered scenes. It first applies
    overlays if requested, and then copies/moves/composes
    individual frames so that an initial set of
    scene1...png, sceneX...png files is converted
    into movie_name...png files that can then
    be merged into a file using ffmpeg.
    :param script: Script instance, the master object controlling the movie layout
    :return: None
    """
    try:
        layout_dirs = script.directives['layout']  # layout controls composition of panels
    except KeyError:
        layout_dirs = None
        nrows = 1
        ncols = 1
    else:
        nrows = int(layout_dirs['rows']) if 'rows' in layout_dirs.keys() else 1
        ncols = int(layout_dirs['columns']) if 'columns' in layout_dirs.keys() else 1
    check_overlays(script)
    for scene in sorted(script.scenes, key=lambda sc: int(sc.is_overlay), reverse=True):
        if scene.contour:
            for fr in range(scene.total_frames):
                img = "{}-{}.png".format(scene.name, fr)
                call_moly('{conv} {img} -canny 0x1+10%+40% -negate -transparent white -blur 0x0.75 border.png; '
                          'composite border.png {img} {img}'.format(conv=script.convert, img=img), log=script.log)
        for action in scene.actions:  # due to sorting, scenes without dependencies should be composed first
            if 'add_overlay' in action.action_type:
                for ovl in action.overlays.keys():
                    if 'scene' in action.overlays[ovl].keys():
                        ovl_scene_name = action.overlays[ovl]['scene']
                        ovl_scene = [sc for sc in script.scenes if sc.name == ovl_scene_name][0]
                        overlay_res = calc_ores(action, ovl, range(ovl_scene.total_frames), True)
                        for fr, ores in zip(range(ovl_scene.total_frames), overlay_res):
                            call_moly('{} {}-{}.png -resize {}x{} '
                                      '{}-{}-{}.png'.format(script.convert, ovl_scene_name, fr, *ores, ovl, scene.name,
                                                            fr + action.initframe), log=script.log)
                compose_overlay(action)

    if nrows * ncols == 1:  # simplest case: one scene
        scene = script.scenes[0].name
        for fr in range(np.max([sc.total_frames for sc in script.scenes])):
            if not (script.restart and os.path.exists('{}-{}.png'.format(script.name, fr))):
                os.rename('{}-{}.png'.format(scene, fr), '{}-{}.png'.format(script.name, fr))

    elif layout_dirs and nrows * ncols > 1:  # here we parse multiple scenes
        # if one has less frames than the other, copy last frame (N-n) times to make counts equal:
        if not all([sc.total_frames == script.scenes[0].total_frames for sc in script.scenes if not sc.is_overlay]):
            equalize_frames(script)
        labels_matrix = [[] for _ in range(nrows)]
        all_scenes = [sc.name for sc in script.scenes]
        positions = {}
        for scene in all_scenes:
            try:
                positions[tuple(int(x) for x in script.directives[scene]['position'].split(','))] = scene
            except KeyError:
                raise ValueError('The position for scene {} in the global layout is not specified'.format(scene))
        for r in range(nrows):
            for c in range(ncols):
                try:
                    scene_name = positions[(r, c)]
                except KeyError:
                    labels_matrix[r].append('')
                else:
                    labels_matrix[r].append(scene_name)
        convert_command = ''
        for r in range(nrows):
            convert_command += ' \( '
            for c in range(ncols):
                convert_command += str(labels_matrix[r][c]) + '-{}.png '
            convert_command += ' +append \) '
        convert_command += ' -append '
        for fr in range(script.scenes[0].total_frames):
            frames = [fr] * (nrows * ncols)
            call_moly(script.convert + ' ' + convert_command.format(*frames) + '{}-{}.png'.format(script.name, fr),
                      log=script.log)

    process_audio(script)


def check_overlays(script):
    """
    Ensures that dependent overlays (i.e. Scenes
    that will be rendered atop other Scenes)
    are properly defined, and calculates level
    of nesting for subsequent ordering of
    rounds of Scene composition
    :param script: Script instance, the master object controlling the movie layout
    :return: None
    """

    def return_dependencies(scn):
        dps = []
        for action in scn.actions:
            if 'add_overlay' in action.action_type:
                for ovl in action.overlays.keys():
                    if 'scene' in action.overlays[ovl].keys():
                        ovl_scene_name = action.overlays[ovl]['scene']
                        try:
                            dps.append([sc for sc in script.scenes if sc.name == ovl_scene_name][0])
                        except IndexError:
                            raise RuntimeError("In action {}, scene={} is not a valid scene "
                                               "identifier".format(action.description, ovl_scene_name))
        return dps

    all_deps = []
    for scene in script.scenes:
        all_deps.extend(return_dependencies(scene))
    indeps = [sc for sc in script.scenes if sc not in all_deps]
    for indep in indeps:
        deps = return_dependencies(indep)
        incr = 1
        while deps:
            new_deps = []
            for dep in deps:
                dep.is_overlay += incr
                new_deps.extend(return_dependencies(dep))
            deps = new_deps[:]
            incr += 1


def gen_fig(action):
    """
    Responsible for frame-by-frame generation of files
    associated with (a) external images and (b)
    on-the-fly generated matplotlib plots
    (essentially any graphics that is not rendered
    by TCL/VMD)
    :param action: Action, object to extract info from
    :return: None
    """
    if 'show_figure' in action.action_type:
        gen_fig_show(action)
    if 'add_overlay' in action.action_type:
        for ovl in action.overlays.keys():
            gen_ovl(action, ovl)


def gen_fig_show(action):
    """
    Generates a static figure whem action is `show_figure`
    :param action: The Action object to draw data from
    :return: None
    """
    convert = action.scene.script.convert
    if 'figure' in action.parameters.keys():
        fig_file = action.parameters['figure']
        fig_file = action.scene.script.check_path(fig_file)
        for fr in range(action.initframe, action.initframe + action.framenum):
            call_moly('{} {} -resize {}x{} {}-{}.png'.format(convert, fig_file, *action.scene.resolution,
                                                             action.scene.name, fr), log=action.scene.script.log)
    elif 'datafile' in action.parameters.keys():
        df = action.parameters['datafile']
        df = action.scene.script.check_path(df)
        data_simple_plot(action, df, 'spl')
        for fr in range(action.initframe, action.initframe + action.framenum):
            fig_file = '{}-{}.png'.format(action.scene.name, fr)
            call_moly('{} spl-{} -resize {}x{} {}'.format(convert, fig_file, *action.scene.resolution, fig_file),
                      log=action.scene.script.log)


def gen_ovl(action, ovl):
    """
    Handles the generation of dynamic overlays (figures,
    text, plots, movies) as requested by `add_overlay`
    :param action: The Action object to draw data from
    :param ovl: str, key for the Action.overlays dictionary
    :return: None
    """
    print("Rendering overlays for scene {}, currently: {}".format(action.scene.name, ovl))
    convert = action.scene.script.convert
    scene = action.scene.name
    res = action.scene.resolution
    frames, actions = calc_frames_ud(action, ovl)
    overlay_res = calc_ores(action, ovl, frames, default=True)
    if 'figure' in action.overlays[ovl].keys():
        fig_file = action.overlays[ovl]['figure']
        fig_file = action.scene.script.check_path(fig_file)
        for fr, ores in zip(frames, overlay_res):
            ovl_file = '{}-{}-{}.png'.format(ovl, scene, fr)
            call_moly('{} {} -resize {}x{} {}'.format(convert, fig_file, *ores, ovl_file), log=action.scene.script.log)
    elif 'datafile' in action.overlays[ovl].keys():
        df = action.overlays[ovl]['datafile']
        df = action.scene.script.check_path(df)
        data_simple_plot(action, df, ovl)
        for fr, ores in zip(frames, overlay_res):
            fig_file = '{}-{}-{}.png'.format(ovl, scene, fr)
            call_moly('{} {} -resize {}x{} {}'.format(convert, fig_file, *ores, fig_file), log=action.scene.script.log)
    elif 'text' in action.overlays[ovl].keys():
        plt.rcParams['mathtext.default'] = 'regular'
        text = action.overlays[ovl]['text']
        scaling_text = ''
        tsize = int(32 * np.sqrt(int(res[0]) * int(res[1])) / (10 ** 3))
        try:
            tsize = int(float(action.overlays[ovl]['textsize']) * tsize)
        except KeyError:
            pass
        textcolors = {'red': 'B22222', 'blue': '2B6CC4', 'green': '008000', 'yellow': 'FFCF48',
                      'orange': 'FF8C00', 'purple': '8F509D'}
        try:
            color = action.overlays[ovl]['textcolor']
        except KeyError:
            tcolor = 'black'
        else:
            try:
                tcolor = '#{}'.format(textcolors[color.lower()])
            except KeyError:
                tcolor = color
        try:
            animation_frames = [float(x) for x in action.overlays[ovl]['dataframes'].split(':')]
            arr = np.linspace(animation_frames[0], animation_frames[1], len(frames))
        except KeyError:
            if '[' in text and ']' in text and '[]' not in text:
                scaling_text = text.split('[')[1].split(']'[0])[0]
                try:
                    _ = [int(x) for x in action.parameters['frames'].split(':')]
                except (KeyError, AttributeError):
                    raise RuntimeError("When the [scaling_factor] syntax is used, an 'animate' action"
                                       "has to specify 'frames' simultaneously")
                else:
                    arr = calc_frames_arr(actions)
            else:
                arr = np.arange(len(frames))
        try:
            fig = plt.figure(figsize=[r / 100 for r in res])
        except RuntimeError:
            plt.switch_backend('agg')
            fig = plt.figure(figsize=[r / 100 for r in res])
        if '[' in text and ']' in text:
            try:
                dpt = action.overlays[ovl]['decimal_points']
            except KeyError:
                dpt = '3'
            for fr in frames:
                newtext = text.replace('[{}]'.format(scaling_text),
                                       '{:.' + dpt + 'f}').format(arr[fr - action.initframe])
                fig_file = '{}-{}-{}.png'.format(ovl, scene, fr)
                plt.clf()
                _ = fig.text(0, 0, newtext, ha='left', va='bottom', size=tsize, color=tcolor)
                plt.savefig(fig_file, transparent=True)
        else:
            templ_file = '{}-{}-x.png'.format(ovl, scene)
            plt.clf()
            _ = fig.text(0, 0, text, ha='left', va='bottom', size=tsize, color=tcolor)
            plt.savefig(templ_file, transparent=True)
            for fr in frames:
                fig_file = '{}-{}-{}.png'.format(ovl, scene, fr)
                copy2(templ_file, fig_file)
            os.remove(templ_file)
    elif 'movie' in action.overlays[ovl].keys():
        basename = '{}-{}-%d.png'.format(ovl, scene)
        movie = action.overlays[ovl]['movie']
        try:
            start = action.overlays[ovl]['from'].rstrip('s')
        except KeyError:
            start = 0
        try:
            time = float(action.overlays[ovl]['length'])
        except KeyError:
            time = action.framenum / action.scene.script.fps
        fps = float(action.framenum) / time
        time += 1 / fps
        timespec = "-ss {} -t {} ".format(start, time)
        call_moly('{} -i {} {} -vf fps={} {} -hide_banner'.format(action.scene.script.ffmpeg, movie, timespec, fps,
                                                                  'tmp_' + basename), log=action.scene.script.log)
        initframe = frames[0]
        totalframes = len(frames)
        for i, ores, n in zip(range(totalframes, 0, -1), overlay_res[::-1], range(totalframes)):
            orig = 'tmp_{ov}-{sc}-{nr}.png'.format(ov=ovl, sc=scene, nr=i)
            modd = '{ov}-{sc}-{fr}.png'.format(ov=ovl, sc=scene, fr=i + initframe - 1)
            if n % 10 == 0:
                print('processing frame {} of movie {}'.format(n, movie))
            call_moly('{} {} -resize {}x{} {}'.format(convert, orig, *ores, modd), log=action.scene.script.log)
            os.remove(orig)


def calc_ores(action, ovl, frames, default=False):
    """
    Calculates per-frame overlay resolutions
    in case relative size is scaled linearly
    :param action: Action or SimultaneousAction instance
    :param ovl: str, name of the overlay
    :param frames: iterable, enumerates all frames overlay should apply to
    :param default: bool, whether a default should be provided or error raised when relative_size is not defined
    :return: list of 2-element lists: [[x_res, y_res] for frame in frames]
    """
    res = action.scene.resolution
    try:
        scaling = action.overlays[ovl]['relative_size']
    except KeyError:
        if default:
            overlay_res = [[r for r in res] for _ in range(len(frames))]
        else:
            raise RuntimeError("With add_overlay, 'relative_size=... has to be specified")
    else:
        if ':' in scaling:
            linear = True if '::' in scaling else False
            scaling = scaling.replace('::', ':')
            initial = float(scaling.split(':')[0])
            final = float(scaling.split(':')[1])
            if linear:
                scale = np.linspace(0, 1, action.framenum)
            else:
                q = np.linspace(-5, 5, action.framenum)
                scale = 1 / (1 + np.exp(-q))
            overlay_res = [[sc * r for r in res] for sc in initial + scale * (final - initial)]
        else:
            overlay_res = [[float(scaling) * r for r in res] for _ in range(action.framenum)]
        if len(frames) > action.framenum:
            overlay_res.extend([overlay_res[-1] for _ in range(len(frames) - action.framenum)])
    return overlay_res


def equalize_frames(script):
    """
    If individual scenes have different frame counts,
    this function appends the corresponding last figure
    to the shorter scenes
    :param script: Script instance, the master object controlling the movie layout
    :return: None
    """
    nframes = [sc.total_frames for sc in script.scenes]
    names = [sc.name for sc in script.scenes]
    highest = max(nframes)
    for n, nf in enumerate(nframes):
        if nf < highest:
            for i in range(nf, highest):
                copy2('{}-{}.png'.format(names[n], nf - 1), '{}-{}.png'.format(names[n], i))


def compose_overlay(action):
    """
    Introduces the overlay provided that the picture
    ('overlay-frame_name.png') was already produced
    and properly scaled by gen_fig
    :param action: Action or SimultaneousAction, object to extract data from
    :return: None
    """
    assert hasattr(action, 'overlays') and isinstance(action.overlays, dict)
    scene = action.scene.name
    res = action.scene.resolution
    for ovl in action.overlays.keys():
        frames, actions = calc_frames_ud(action, ovl)
        try:
            sigmoid = action.overlays[ovl]['sigmoid']
        except KeyError:
            sigmoid = False
        else:
            sigmoid = True if sigmoid.lower() in ['true', 't', 'y', 'yes'] else False
        if sigmoid:
            sgm_frames_init = int(0.2 * action.framenum)
            sgm_frames_final = int(0.2 * actions[-1].framenum)
            x_init = np.linspace(-5, 0, sgm_frames_init)
            x_final = np.linspace(0, 5, sgm_frames_final)
            sgm_init = 1 / (1 + np.exp(-x_init))
            sgm_final = 1 / (1 + np.exp(-x_final))
            opacity = np.concatenate((sgm_init, np.ones(len(frames) - (sgm_frames_init + sgm_frames_final)),
                                      sgm_final[::-1]))
        else:
            opacity = np.ones(len(frames))
        try:
            ori_x, ori_y = action.overlays[ovl]['origin'].split(',')
        except KeyError:
            origin_frac = [[0, 0] for _ in range(len(frames))]
        else:
            def get_range(ori):
                linear = True if '::' in ori else False
                if ':' in ori:
                    ori = ori.replace('::', ':')
                    initial = float(ori.split(':')[0])
                    final = float(ori.split(':')[1])
                else:
                    initial = final = float(ori)
                return linear, ori, initial, final

            linear_x, ori_x, initial_x, final_x = get_range(ori_x)
            linear_y, ori_y, initial_y, final_y = get_range(ori_y)
            if linear_x:
                scale_x = np.linspace(0, 1, action.framenum)
            else:
                q = np.linspace(-5, 5, action.framenum)
                scale_x = 1 / (1 + np.exp(-q))
            if linear_y:
                scale_y = np.linspace(0, 1, action.framenum)
            else:
                q = np.linspace(-5, 5, action.framenum)
                scale_y = 1 / (1 + np.exp(-q))
            origin_frac = [[x, y] for x, y in zip(initial_x + scale_x * (final_x - initial_x),
                                                  initial_y + scale_y * (final_y - initial_y))]
            if len(frames) > action.framenum:
                origin_frac.extend([origin_frac[-1] for _ in range(len(frames) - action.framenum)])
        transp_bg = True if 'transparent_background' in action.overlays[ovl].keys() \
                            and action.overlays[ovl]['transparent_background'] in ['true', 't', 'y', 'yes'] else False
        try:
            alpha = action.overlays[ovl]['alpha']
        except KeyError:
            alpha = np.ones(action.framenum)
        else:
            if ':' in alpha:
                linear_a = True if '::' in alpha else False
                alpha = alpha.replace('::', ':')
                if linear_a:
                    alpha = np.linspace(float(alpha.split(':')[0]), float(alpha.split(':')[1]), action.framenum)
                else:
                    q = np.linspace(-5, 5, action.framenum)
                    sgm = 1 / (1 + np.exp(-q))
                    alpha = float(alpha.split(':')[0]) + sgm * (float(alpha.split(':')[1]) - float(alpha.split(':')[0]))
            else:
                alpha = float(alpha) * np.ones(len(frames))
        if len(frames) > action.framenum:
            alp = [alpha]
            for ac in actions[1:-1]:
                if ac.framenum > 0:
                    alp.append(np.ones(ac.framenum) * alp[-1][-1])
            completed = False
            if hasattr(actions[-1], 'overlays'):
                if ovl in actions[-1].overlays.keys():
                    if actions[-1].overlays[ovl]['mode'] == 'd':
                        if 'alpha' in actions[-1].overlays[ovl].keys():
                            alp2 = actions[-1].overlays[ovl]['alpha']
                            if ':' in alp2:
                                alp.append(np.linspace(float(alp2.split(':')[0]), float(alp2.split(':')[1]),
                                                       actions[-1].framenum))
                            else:
                                alp.append(np.ones(actions[-1].framenum) * np.array([float(alp2)]))
                            completed = True
            if not completed:
                alp.append(np.ones(actions[-1].framenum) * alp[-1][-1])
            alpha = np.concatenate(alp)
        origin_px = [[int(r * o) for r, o in zip(res, ofr)] for ofr in origin_frac]
        for fr, opa, al, opx in zip(frames, opacity, alpha, origin_px):
            if fr % 10 == 0:
                print('composing frame {} of scene {} with {}'.format(fr, action.scene.name, ovl))
            fig_file = '{}-{}-{}.png'.format(ovl, scene, fr)
            target_fig = '{}-{}.png'.format(scene, fr)
            opa *= al
            if transp_bg:
                call_moly('{} {} -transparent white {}'.format(action.scene.script.convert, fig_file, fig_file),
                          log=action.scene.script.log)
            if opa != 1:
                call_moly('{} {} -alpha set -channel a -evaluate multiply {} '
                          '+channel {}'.format(action.scene.script.convert, fig_file, opa, fig_file),
                          log=action.scene.script.log)
            call_moly('{} -gravity SouthWest -compose atop -geometry +{}+{} '
                      '{} {} {}'.format(action.scene.script.compose, *opx, fig_file, target_fig, target_fig),
                      log=action.scene.script.log)


def data_simple_plot(action, datafile, basename):
    """
    Creates a set of customizable 1D line plots
    or 2D hexbin plots based on a provided data file
    to e.g. accompany the display of an
    animated trajectory
    :param action: Action or SimultaneousAction, object to extract data from
    :param datafile: str, file containing the data to be plotted
    :param basename: str, base name of the image to be produced (e.g. 'overlay1')
    :return: None
    """
    font = {'size': 18}
    plt.rc('font', **font)
    plt.rc('axes', linewidth=2)
    res = action.scene.resolution
    frames, actions = calc_frames_ud(action, basename)
    try:
        asp_ratio = float(action.parameters['aspect_ratio'])
    except KeyError:
        asp_ratio = res[0] / res[1]
    plt.rcParams['figure.figsize'] = [4.8 * np.sqrt(asp_ratio), 4.8 / np.sqrt(asp_ratio)]
    try:
        plt.clf()
        fig = plt.figure()
    except RuntimeError:
        plt.switch_backend('agg')
        plt.clf()
        fig = plt.figure()
    try:
        animation_frames = [int(x) for x in action.overlays[basename]['dataframes'].split(':')]
        arr = np.linspace(animation_frames[0], animation_frames[1], len(frames)).astype(int)
    except KeyError:
        try:
            arr = np.loadtxt(action.overlays[basename]['dataframes_from_file']).reshape(-1).astype(int)
        except KeyError:
            try:
                _ = [int(x) for x in action.parameters['frames'].split(':')]
            except (KeyError, AttributeError):
                draw_point, arr = False, None
            else:
                arr = calc_frames_arr(actions)
    draw_point = True
    datasets = []
    flag_setup = False
    raw_data = [line.strip() for line in open(datafile) if line.strip()]
    for line in raw_data:
        if not flag_setup and (line.startswith('#') or line.startswith('!')):
            flag_setup = True
            datasets.append({'setup': [], 'data': []})
        if not datasets:
            datasets.append({'setup': [], 'data': []})
        if flag_setup and not (line.startswith('#') or line.startswith('!')):
            flag_setup = False
        if flag_setup:
            datasets[-1]['setup'].append(line)
        else:
            datasets[-1]['data'].append([float(x) for x in line.split()])
    xmin, ymin, xmax, ymax = np.infty, np.infty, -np.infty, -np.infty
    labels = False
    for dset in datasets:
        dset['data'] = np.array(dset['data'])
        try:
            labels = [x.strip() for x in dset['setup'] if x.strip().startswith('#')][0]
        except IndexError:
            pass
        else:
            labels = labels.strip('#').strip().split(';')
        try:
            mpl_kw = [x.strip() for x in dset['setup'] if x.strip().startswith('!')][0]
        except IndexError:
            mpl_kw = {}
        else:
            mpl_kw = {x.split('=')[0]: x.split('=')[1] for x in mpl_kw.strip('!').strip().split()}
            for kw in mpl_kw.keys():
                try:
                    mpl_kw[kw] = eval(mpl_kw[kw])
                except:
                    pass
        if 'xlim' not in mpl_kw.keys():
            xmin = np.min(dset['data'][:, 0]) if np.min(dset['data'][:, 0]) < xmin else xmin
            xmax = np.max(dset['data'][:, 0]) if np.max(dset['data'][:, 0]) > xmax else xmax
        else:
            xmin, xmax = mpl_kw['xlim']
            mpl_kw.pop('xlim')
        if 'ylim' not in mpl_kw.keys():
            ymin = np.min(dset['data'][:, 1]) if np.min(dset['data'][:, 1]) < ymin else ymin
            ymax = np.max(dset['data'][:, 1]) if np.max(dset['data'][:, 1]) > ymax else ymax
        else:
            ymin, ymax = mpl_kw['ylim']
            mpl_kw.pop('ylim')
        dset['mpl'] = {}
        dset['mpl'].update(mpl_kw)
    if not labels:
        labels = ['Time', 'Value']
    if '2D' in action.overlays[basename].keys() and action.overlays[basename]['2D'].lower() in ['t', 'y',
                                                                                                'true', 'yes']:
        if ('seaborn' in action.overlays[basename].keys() and
                action.overlays[basename]['seaborn'].lower() in ['t', 'y', 'true', 'yes']):
            seaborn = True
        else:
            seaborn = False
            ax = fig.add_subplot(1, 1, 1)
        for dset in datasets:
            grid_x = np.min([int(np.sqrt(len(dset['data']) * asp_ratio) / 2), 100])
            grid_y = np.min([int(grid_x / asp_ratio), 100])
            if 'gridsize' not in dset['mpl'].keys():
                dset['mpl'].update({'gridsize': (grid_x, grid_y)})
            if 'bins' not in dset['mpl'].keys():
                dset['mpl'].update({'bins': 'log'})
            if 'mincnt' not in dset['mpl'].keys():
                dset['mpl'].update({'mincnt': 1})
            if seaborn:
                alpha = 0.6 if len(datasets) > 1 else 1
                ax = sns.kdeplot(*dset['data'].T, shade=True, shade_lowest=False, alpha=alpha)
            else:
                ax.hexbin(*dset['data'].T, zorder=0, **dset['mpl'])
    else:
        ax = fig.add_subplot(1, 1, 1)
        for dset in datasets:
            if 'lw' not in dset['mpl'].keys() and 'linewidth' not in dset['mpl'].keys():
                dset['mpl'].update({'lw': 3})
            if dset['data'].shape[1] <= 2:
                ax.plot(*dset['data'].T, zorder=0, **dset['mpl'])
            else:
                for col in range(dset['data'].shape[1] - 1):
                    ax.plot(dset['data'][:, 0], dset['data'][:, 1 + col], zorder=col, **dset['mpl'])
        ax.set_xlim(1.1 * xmin, 1.1 * xmax)
        ax.set_ylim(1.1 * ymin, 1.1 * ymax)
    xticks, xlim = ax.get_xticks(), ax.get_xlim()  # prevents ticks/scaling from changing from frame to frame
    yticks, ylim = ax.get_yticks(), ax.get_ylim()  # which would normally happen with tight_layout
    for fr in frames:
        count = fr - action.initframe
        pts_drawn = 0
        if draw_point:
            for dset in datasets:
                for col in range(dset['data'].shape[1] - 1):
                    if dset['data'].shape[1] == 2:
                        pt_color = 'C3'
                    else:
                        pt_color = 'C' + str(col)
                    try:
                        ax.scatter(dset['data'][arr[count], 0], dset['data'][arr[count], 1 + col],
                                   s=250, zorder=1, c=pt_color)
                    except IndexError:
                        pass
                    else:
                        pts_drawn += 1
        ax.set_xlim(xlim)
        ax.set_xticks(xticks)
        ax.set_ylim(ylim)
        ax.set_yticks(yticks)
        ax.set_xlabel(labels[0])
        ax.set_ylabel(labels[1])
        plt.tight_layout(pad=0.5)
        plt.savefig('{}-{}-{}.png'.format(basename, action.scene.name, fr))
        for pt in range(pts_drawn):
            ax.collections.pop()


def calc_frames_ud(action, ovl):
    """
    If an action can have modes up (u), down (d) or up-down (ud),
    this function will match 'ups' with 'downs' to return the
    frame numbers and Actions covered by the current action's span
    :param action: Action, contains at least one add_overlay
    :param ovl: str, name of the overlay
    :return: iterator, enumerates frames spanned by the action
             list, contains Actions affected by the overlay
    """
    try:
        mode = action.overlays[ovl]['mode']
    except KeyError:
        mode = 'ud'
    else:
        if mode not in ['u', 'd', 'ud']:
            raise RuntimeError("In {}, mode should be 'u', 'd' or 'ud'".format(action.description))
    if mode == 'ud':
        return range(action.initframe, action.initframe + action.framenum), [action]
    elif mode == 'u':
        action_index = action.scene.actions.index(action)
        try:
            alias = action.overlays[ovl]['alias']
        except KeyError:
            return range(action.initframe, action.scene.total_frames), action.scene.actions[action_index:]
        else:
            for act in action.scene.actions[action_index:]:
                try:
                    ovls = list(act.overlays.keys())
                except AttributeError:
                    ovls = []
                for ov in ovls:
                    try:
                        als = act.overlays[ov]['alias']
                    except KeyError:
                        pass
                    else:
                        try:
                            md = act.overlays[ov]['mode']
                        except KeyError:
                            pass
                        else:
                            if als == alias and md == 'd':
                                action_index_last = action.scene.actions.index(act)
                                return range(action.initframe, act.initframe + act.framenum), \
                                    action.scene.actions[action_index:action_index_last + 1]
            return range(action.initframe, action.scene.total_frames), action.scene.actions[action_index:]
    elif mode == 'd':
        return range(0), []


def calc_frames_arr(actions):
    arrs = []
    for ac in actions:
        try:
            animation_frames = [int(x) for x in ac.parameters['frames'].split(':')]
        except KeyError:
            animation_frames = 2 * [arrs[-1][-1]]
        if ac.framenum > 0:
            arrs.append(np.linspace(animation_frames[0], animation_frames[1], ac.framenum).astype(int))
    return np.concatenate(arrs)


def process_audio(scr):
    """
    Processes directives for the `add_audio` Action,
    yielding a list of relevant variables like starting
    poits, segment length, name of the file etc. then
    sorts the segments according to their starting times
    :param scr: The top-level Script object
    :return: None
    """
    for scene in scr.scenes:
        for action in scene.actions:
            if 'add_audio' in action.action_type:
                try:
                    audiofile = action.parameters['audiofile']
                except KeyError:
                    raise RuntimeError("To add a soundtrack, specify the audio file using 'audiofile=...'")
                else:
                    if not os.path.exists(os.path.expanduser(audiofile)):
                        raise RuntimeError("Audio file {} was not found in your filesystem".format(audiofile))
                try:
                    starttime = float(action.parameters['from'])
                except KeyError:
                    starttime = 0
                try:
                    length = float(action.parameters['length'])
                except KeyError:
                    length = 3600
                try:
                    volume = float(action.parameters['volume'])
                except KeyError:
                    volume = 1.0
                try:
                    fin = float(action.parameters['fade_in'])
                except KeyError:
                    fin = 1.0
                try:
                    fout = float(action.parameters['fade_out'])
                except KeyError:
                    fout = 1.0
                tp = namedtuple("audio", "audiofile, movie_inittime, file_inittime, length, volume, fadein, fadeout")
                scr.audio.append(tp(audiofile, action.initframe/scr.fps, starttime, length, volume, fin, fout))
    scr.audio.sort(key=lambda x: x[1])


def call_moly(arg, answer=False, log=False):
    """
    A wrapper to consistently take care of all external calls
    :param arg: str, a command to be run from the command line
    :param answer: bool, whether to return the captured output
    :param log: bool, whether to log the command to a file
    :return: str, captured output from the command
    """
    result = call(arg, shell=True)
    if log:
        with open('command_line_log.moly', 'a') as outfile:
            outfile.write(arg + '\n')
    if answer:
        return result
