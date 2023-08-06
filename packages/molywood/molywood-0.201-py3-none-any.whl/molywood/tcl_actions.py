import os
try:
    import numpy as np
except ImportError:
    pass
from collections import OrderedDict


def sigmoid_increments(n_points, abruptness):
    """
    Returns stepwise increments that result in logistic
    growth from 0 to sum over n_points
    :param n_points: int, number of increments
    :param abruptness: float, how fast the transition is
    :return: numpy.array, array of increments
    """
    scale_range = (-5, 5)
    points = np.linspace(*scale_range, n_points)
    increments = logistic_deriv(points, abruptness)
    return increments
    

def sigmoid_norm_sum(cumsum, n_points, abruptness=1):
    """
    Yields n_points increments that sum to cumsum
    :param cumsum: float, cumulative sum of the increments
    :param n_points: int, number of increments
    :param abruptness: float, how fast the transition is
    :return: numpy.array, array of increments
    """
    increments = sigmoid_increments(n_points, abruptness)
    return cumsum*increments/np.sum(increments)


def sigmoid_norm_prod(cumprod, n_points, abruptness=1):
    """
    Yields n_points increments that multiply to cumprod
    :param cumprod: float, cumulative sum of the increments
    :param n_points: int, number of increments
    :param abruptness: float, how fast the transition is
    :return: numpy.array, array of increments
    """
    increments = np.array(1) + sigmoid_increments(n_points, abruptness)
    prod = np.prod(increments)
    exponent = np.log(cumprod)/np.log(prod)
    return increments**exponent


def sigmoid_norm_sum_linear_mid(cumsum, n_points, abruptness=1, fraction_linear=0.4):
    """
    Yields n_points increments that sum to cumsum
    by first starting with smooth sigmoid increments,
    then incrementing linearly, and then stopping
    smoothly again with sigmoid increments
    (e.g. we want to rotate more or less continuously
    by 720deg about an axis, but start and finish smoothly)
    :param cumsum: float, cumulative sum of the increments
    :param n_points: int, number of increments
    :param abruptness: float, how fast the transition is
    :param fraction_linear: float, fraction of the action spent in the linear regime
    :return: numpy.array, array of increments
    """
    n_points_sigm = int(n_points * (1-fraction_linear))
    n_points_linear = n_points - n_points_sigm
    increments = sigmoid_increments(n_points_sigm, abruptness)
    midpoint = len(increments)//2
    midpoint_increment = increments[midpoint]
    increments = np.concatenate((increments[:midpoint],
                                 np.ones(n_points_linear)*midpoint_increment,
                                 increments[midpoint:]))
    return cumsum * increments / np.sum(increments)


def logistic(x, k):
    """
    The logistic fn used to smoothen transitions
    :param x: abscissa
    :param k: transition abruptness
    :return: numpy.array, values of the logistic fn
    """
    return np.array(1/(1+np.exp(-k*x)))


def logistic_deriv(x, k):
    """
    Derivative of the logistic fn used to smoothen transitions
    (in a discretized version yields single-step increments)
    :param x: abscissa
    :param k: transition abruptness
    :return: numpy.array, values of the logistic fn derivative
    """
    logi = logistic(x, k)
    return np.array(logi*(1-logi))


def gen_loop(action):
    """
    The main fn that generates TCL code (mostly loops,
    hence the name). We mostly use three-letter names for
    variables/dict entries according to the convention:
    center_view -> ctr;
    rotate -> rot;
    zoom_in/zoom_out -> zin/zou;
    animate -> ani etc.
    :param action: Action or SimultaneousAction, object to extract info from
    :return: str, formatted TCL code
    """
    if 'insert_tcl' in action.action_type:
        print("Inserting user's TCL code. In case of issues, look up {}_vmdlog.moly for error "
              "messages".format(action.scene.name))
        if 'file' in action.parameters.keys() or 'code' in action.parameters.keys():
            try:
                file = action.parameters['file']
            except KeyError:
                try:
                    code = action.parameters['code'] + '\n'
                except KeyError:
                    raise RuntimeError("'insert_tcl' requires a 'file=...' or 'code=...' parameter")
                else:
                    return code
            return ''.join(open(file).readlines()) + '\n'
    setup = gen_setup(action)
    iterators = gen_iterators(action)
    if 'insert_tcl' in action.action_type and \
            ('range' in action.parameters.keys() or 'loopover' in action.parameters.keys()):
        try:
            start, end = action.parameters['range'].split(':')  # TODO check
        except KeyError:
            if ',' in action.parameters['loopover']:
                iter_list = action.parameters['loopover'].split(',')
            else:
                iter_list = action.parameters['loopover'].split()
            if len(iter_list) != action.framenum:  # we resample from the user-provided list if numbers don't match
                loopover = [iter_list[int(i // (action.framenum/len(iter_list)))] for i in range(action.framenum)]
            else:
                loopover = iter_list
            loopover = ' '.join(loopover)
        else:
            loopover = ' '.join(str(x) for x in np.linspace(float(start), float(end), action.framenum))
        iterators.update({'tcl': loopover})
    command = gen_command(action)
    if 'insert_tcl' in action.action_type and 'loop_command' in action.parameters.keys():
        select = "set t [lindex $tcl $i]\n  "
        command.update({'tcl': select + action.parameters['loop_command'].replace('{}', '$t') + '\n'})
    cleanups = gen_cleanup(action)
    code = "\n\nset fr {}\n".format(action.initframe)
    res = ' '.join(str(x) for x in action.scene.resolution)
    for act in setup.keys():
        code = code + setup[act]
    for act in iterators.keys():
        code += 'set {} [list {}]\n'.format(act, iterators[act])
    if action.framenum > 0:
        code += 'for {{set i 0}} {{$i < {}}} {{incr i}} {{\n'.format(action.framenum)
        for act in command.keys():
            code = code + '  ' + command[act]
        if action.scene.script.do_render:
            code += '  puts "rendering frame: $fr"\n  display resize {res}\n'.format(res=res)
            if action.already_rendered:
                code += '  puts "skipping already rendered frame $fr"\n'
            elif action.scene.draft:
                code += '  render snapshot {sc}-$fr.tga\n'.format(sc=action.scene.name)
            else:
                if not action.scene.script.tachyon:
                    tach = '$env(TACHYON_BIN)'
                    remove = 'rm'
                else:
                    tach = action.scene.script.tachyon.replace('\\', '\\\\')
                    remove = 'cmd.exe /c del'
                code += '  render Tachyon {sc}-$fr.dat\n  \"{tc}\" ' \
                        '-aasamples 12 {sc}-$fr.dat -format TARGA -o {sc}-$fr.tga -trans_max_surfaces {tm} -res {rs}' \
                        '\n  exec {rm} {sc}-$fr.dat\n'.format(sc=action.scene.name, tc=tach, rm=remove,
                                                              tm=action.scene.transparent_surfaces,
                                                              rs=' '.join(str(x) for x in action.scene.resolution))
            if 'do_nothing' in action.action_type and not action.already_rendered:
                if os.name == 'posix':
                    copy = 'cp'
                else:
                    copy = 'cmd.exe /c copy'
                code += 'set tmpfr $fr\n'
                code += 'for {{set i 1}} {{$i < {fr}}} {{incr i}} {{incr fr; {copy} {sc}-$tmpfr.tga {sc}-$fr.tga}}; ' \
                        'break\n'.format(fr=action.framenum, copy=copy, sc=action.scene.name)
        else:
            code += '  puts "frame: $fr"\n  after {aft}\n  display resize {res}\n  display update' \
                    '\n'.format(aft=str(int(1000/action.scene.script.fps)), res=res)
        code += '  incr fr\n}\n'
    for act in cleanups.keys():
        code = code + cleanups[act]
    return code


def gen_setup(action):
    """
    Some actions (e.g. centering) require a setup step that
    only has to be performed once; this fn is supposed
    to take care of such thingies
    :param action: Action or SimultaneousAction, object to extract info from
    :return: dict, formatted as label: command
    """
    setups = OrderedDict()
    materials = materials_dict()
    if 'center_view' in action.action_type:
        try:
            mols = action.parameters['molecules']
        except KeyError:
            mols = -2
        else:
            if mols == 'all':
                mols = -2
            elif mols == 'top':
                mols = -1
            else:
                try:
                    _ = [int(x) for x in mols.split(',')]
                except ValueError:
                    raise RuntimeError("With center_view, 'molecules' should be 'all', 'top' or a string "
                                       "of comma-separated integers")
                else:
                    mols = ' '.join(mols.split(','))
        try:
            new_center_selection = action.parameters['selection']
        except KeyError:  # TODO test
            raise ValueError('With center_view, you need to specify a selection (vmd-compatible syntax, in quot marks)')
        else:
            setups['ctr'] = 'set top {}\nif {{$top == -1}} {{set topmol [molinfo top]; set listmol [list $topmol]}} ' \
                            'elseif {{$top == -2}} {{set listmol [molinfo list]}} else {{set listmol [split $top]}}\n' \
                            'foreach ml $listmol {{' \
                            'set csel [atomselect $ml "{}"]\nset gc [veczero]\nforeach coord [$csel get {{x y z}}] ' \
                            '{{\n  set gc [vecadd $gc $coord]\n}}\n' \
                            'set cent [vecscale [expr 1.0 /[$csel num]] $gc]\n' \
                            'molinfo $ml set center [list $cent]}}\n'.format(mols, new_center_selection)
    if 'add_label' in action.action_type:
        try:
            label_color = action.parameters['label_color']
        except KeyError:
            label_color = 'black'
        try:
            tsize = action.parameters['text_size']
        except KeyError:
            tsize = 1.0
        else:
            check_if_convertible(tsize, float, 'text_size')
        if not action.scene.draft:  # there's a slight difference in text size between Tachyon and Snapshot
            tsize = float(tsize) * 0.75
        try:
            alias = action.parameters['alias']
        except KeyError:
            alias = 'label{}'.format(len(action.scene.labels['Atoms'])+1)
        try:
            offset = action.parameters['offset']
        except KeyError:
            offset_command = ''
        else:
            offs_x, offs_y = offset.split(',')
            check_if_convertible(offs_x, float, 'offset_x')
            check_if_convertible(offs_y, float, 'offset_y')
            offset_command = 'label textoffset Atoms $nlab {{ {} {} }}'.format(offs_x, offs_y)
        action.scene.labels['Atoms'].append(alias)
        atom_index = action.parameters['atom_index']  # use selection as in distance?
        label = action.parameters['label']
        check_if_convertible(atom_index, int, 'atom_index')
        setups['adl'] = 'set nlab [llength [label list Atoms]]\n' \
                        'set currtop [molinfo top]\n' \
                        'label add Atoms $currtop/{}\n' \
                        'label textsize {}\n' \
                        'label textthickness 1.75\n' \
                        'color Labels Atoms {}\n' \
                        'label textformat Atoms $nlab "{}"\n' \
                        '{}\n\n'.format(atom_index, tsize, label_color, label, offset_command)
    if 'remove_label' in action.action_type or 'remove_distance' in action.action_type:
        lab_type = 'Atoms' if 'remove_label' in action.action_type else 'Bonds'
        remove_all = False
        try:
            alias = action.parameters['alias']
        except KeyError:
            alias = ''
            try:
                remove_all = action.parameters['all']
            except KeyError:
                raise RuntimeError('To remove a label, either "all=t" or "alias=..." have to be specified')
            else:
                if remove_all in ['y', 't', 'yes', 'true']:
                    remove_all = True
                else:
                    raise RuntimeError('To remove a label, either "all=t" or "alias=..." have to be specified')
        if alias:
            try:
                alias_index = action.scene.labels[lab_type].index(alias)
            except ValueError:
                raise RuntimeError('"{}" is not a valid alias; to remove a label, alias has to match a previously added'
                                   'one'.format(alias))
            else:
                action.scene.labels[lab_type].pop(alias_index)
                setups['rml'] = 'set molnum_bond [lindex [label list Bonds] {} 0 0]\n' \
                                'mol off $molnum_bond\n' \
                                'label delete {} {}\n'.format(alias_index, lab_type, alias_index)
        elif remove_all:
            nlab = len(action.scene.labels[lab_type])
            setups['rml'] = nlab * 'label delete {} 0\n'.format(lab_type)
            action.scene.labels[lab_type] = []
    if 'add_distance' in action.action_type:
        try:
            label_color = action.parameters['label_color']
        except KeyError:
            label_color = 'black'
        try:
            tsize = action.parameters['text_size']
        except KeyError:
            tsize = 1.0
        else:
            check_if_convertible(tsize, float, 'text_size')
        try:
            bead = True if action.parameters['bead'].lower() in ['y', 't', 'yes', 'true'] else False
        except KeyError:
            bead = False
        if bead:
            bead = 'mol representation VDW 1.200000 25.000000\nmol color ColorID 8\n'
        else:
            bead = 'mol representation Lines\n'
        try:
            alias = action.parameters['alias']
        except KeyError:
            alias = 'label{}'.format(len(action.scene.labels['Bonds'])+1)
        action.scene.labels['Bonds'].append(alias)
        sel1 = action.parameters['selection1']
        sel2 = action.parameters['selection2']
        setups['add'] = 'package require multiseq\n' \
                        'save_vp 1\n' \
                        'set currframe [molinfo top get frame]\n\n'
        setups['add'] += add_once(geom_center, action)  # TODO big thing: per-molecule highlights
        setups['add'] += add_once(retr_vp, action)  # TODO check top and re-select mol as top after dummies are built
        setups['add'] += 'set currtop [molinfo top]\n' \
                         'set newmol{} [mol new atoms 2]\n{}' \
                         'mol selection all\n' \
                         'mol addrep $newmol{}\n' \
                         'label add Bonds $newmol{}/0 $newmol{}/1\n' \
                         'color Labels Bonds {}\n' \
                         'label textsize {}\n' \
                         'label textthickness 3\n' \
                         'mol top $currtop\n\n'.format(alias, bead, alias, alias, alias, label_color, tsize)
        setups['add'] += reposition_dummies(sel1, sel2)
        setups['add'] += 'set num_steps [molinfo top get numframes]\n' \
                         'for {{set frame 0}} {{$frame < $num_steps}} {{incr frame}} {{\n' \
                         '  animate goto $frame\n' \
                         '  reposition_dummies $newmol{}}}\n\n'.format(alias)
        setups['add'] += 'animate goto $currframe\n\n' \
                         'display resetview\n'
        setups['add'] += 'retr_vp 1\n'  # re-align all after display resetview
    if 'highlight' in action.action_type:
        colors = colors_dict()
        hls = [action.highlights[x] for x in action.highlights.keys()]
        hl_labels = list(action.highlights.keys())
        for lb, hl in zip(hl_labels, hls):
            setups[lb] = ''
            try:
                mode = hl['mode']
            except KeyError:
                hls = find_highlights_with_alias(action, hl)
                hls_upto = [h for h in hls[:hls.index(hl)]] if hls else False
                if hls_upto:
                    mode = 'n'
                else:
                    mode = 'ud'
            if mode == 'n' and 'alias' not in hl.keys():
                raise RuntimeError("When 'mode' is 'n', you need to provide the alias of the highlight you're changing")
            try:
                cutoff = hl['cutoff']
            except KeyError:
                cutoff = 1.6
            else:
                cutoff = check_if_convertible(cutoff, float, 'cutoff')
            try:
                material_hl = hl['material'].lower()
            except KeyError:
                material_hl = 'Opaque'
            else:
                try:
                    material_hl = materials[material_hl]
                except KeyError:
                    pass
            if mode in ['u', 'ud']:
                setups[lb] += 'material add copy {}\n' \
                              'set mat{} [lindex [material list] end]\n' \
                              'material change opacity $mat{} 0\n'.format(material_hl, lb, lb)
            try:
                color_key = hl['color']
            except KeyError:
                color_key = 'red'
            else:
                if '-' in color_key:
                    color_directives = color_key.split('-')[1:]
                    color_key = color_key.split('-')[0]
                    if color_key.lower() not in ['type', 'name', 'element']:
                        raise RuntimeError("Changing default colors is only available for coloring schemes: Type, Name"
                                           " and Element")
                    for spec in color_directives:
                        if spec.count(':') != 1:
                            raise RuntimeError("To change default color schemes, use the syntax scheme-element1:color1-"
                                               "element2:color2-... etc. in your 'highlight' parameters")
                        element, color = spec.split(':')
                        setups[lb] += 'color {} {} {}\n'.format(color_key.title(), element.title(), color.lower())
            try:
                style = hl['style'].lower()  # parse as lowercase to avoid confusion among users
            except KeyError:
                style = 'newcartoon'
            if style == 'isosurface':
                try:
                    isovalue = hl['isovalue']
                except KeyError:
                    raise RuntimeError("To use isosurface-based highlights, provide a corresponding isovalue=...")
                else:
                    isovalue = float(isovalue.split(':')[0])
            else:
                isovalue = 0
            if 'multiframe' in action.parameters and hl['multiframe'].lower() == 'now':
                setups[lb] += 'mol drawframes top [lindex $repnums $repnum_{}] now\n'.format(lb)
            try:
                thick = hl['thickness']
            except KeyError:
                thick = 1.0
            else:
                if not mode == 'n':
                    check_if_convertible(thick, float, 'thickness')
                    thick = float(thick)
                else:
                    thick = 1.0  # will be processed elsewhere anyway
            style_params = {'newcartoon': ['NewCartoon', '{} 30 4.1 0'.format(0.32*thick)],
                            'surf': ['Surf', '1.4 0.0'],
                            'quicksurf': ['QuickSurf', '0.9 {} 0.5 3.0'.format(1.3/thick)],
                            'licorice': ['Licorice', '{} 12.0 12.0'.format(0.31*thick)],
                            'vdw': ['VDW', '{} 20.0'.format(1.05*thick)],
                            'dynamicbonds': ['DynamicBonds', '{} {} 12.0'.format(cutoff, 0.31*thick)],
                            'tube': ['Tube', '{} 20.0'.format(0.40*thick)],
                            'isosurface': ['Isosurface', '{} 0 0 0 1 1'.format(isovalue)]}
            if style not in style_params.keys():
                raise RuntimeError('{} is not a valid style; "NewCartoon", "Surf", "QuickSurf", "VDW", "Tube", '
                                   '"Isosurface" and "Licorice" are available'.format(style))
            if color_key in colors.keys():
                cl = 'ColorID {}'.format(colors[color_key])
            else:
                try:
                    cl = 'ColorID {}'.format(int(color_key))
                except ValueError:
                    avail_schemes = {"name": "Name", "type": "Type", "resname": "ResName", "restype": "ResType",
                                     "resid": "ResID", "element": "Element", "molecule": "Molecule",
                                     "structure": "Structure", "chain": "Chain", "beta": "Beta",
                                     "occupancy": "Occupancy", "mass": "Mass", "charge": "Charge", "pos": "Pos"}
                    if color_key.lower() in avail_schemes.keys():
                        cl = avail_schemes[color_key]
                    else:
                        raise RuntimeError('{} is not a valid color description'.format(color_key))
            if mode in ['u', 'ud']:
                if 'isovalue' in hl.keys():
                    sel_string = ''
                else:
                    sel = hl['selection']
                    sel_string = 'mol selection {{{}}}\n'.format(sel)
                setups[lb] += 'mol representation {} {}\n' \
                              'mol color {}\n' \
                              'mol material $mat{}\n' \
                              '{}' \
                              'set repnum_{} [llength $repnums]\n' \
                              'mol selupdate $repnum_{} top 1\n' \
                              'lappend repnums [molinfo top get numreps]\n' \
                              'mol addrep top\n'.format(*style_params[style], cl, lb, sel_string, lb, lb)
            try:
                smooth = action.parameters['smooth']
            except KeyError:
                pass
            else:
                check_if_convertible(smooth, int, 'smooth')
                setups[lb] += 'set mtop [molinfo top]\nset nrep [molinfo $mtop get numreps]\n' \
                              'mol smoothrep $mtop $nrep\n'.format(smooth)
        if action.framenum == 0:
            for lb, hl in zip(hl_labels, hls):
                mode = hl['mode'] if 'mode' in hl.keys() else 'ud'
                alpha = float(hl['alpha']) if 'alpha' in hl.keys() else 1
                if mode == 'd':
                    try:
                        _ = hl['alias']
                    except KeyError:
                        raise RuntimeError('When mode=d, an alias has to be supplied to specify which highlight'
                                           'has to be turned off.')
                    setups[lb] += "material change opacity $mat{} 0\n".format(lb)
                elif mode in ['u', 'ud']:
                    setups[lb] += "material change opacity $mat{} {}\n".format(lb, alpha)
                else:
                    pass
    if 'fit_trajectory' in action.action_type:
        sel = action.parameters['selection']  # TODO make work for multiple molecules
        try:
            mols = action.parameters['molecules']
        except KeyError:
            mols = -2
        else:
            if mols == 'all':
                mols = -2
            if mols == 'top':
                mols = -1
            else:
                try:
                    _ = [int(x) for x in mols.split(',')]
                except ValueError:
                    raise RuntimeError("With fit_trajectory, 'molecules' should be 'all', 'top' or a string "
                                       "of comma-separated integers")
                else:
                    mols = ' '.join(mols.split(','))
        try:
            axis = action.parameters['axis']
        except KeyError:
            axis = None
            setups['ftr'] = ''
        else:
            try:
                invert = action.parameters['invert']
            except KeyError:
                invert = False
            else:
                invert = True if invert.lower() in ['t', 'y', 'true', 'yes'] else False
            if axis.lower() == 'z':
                axis = '0 0 1'
            elif axis.lower() == 'y':
                axis = '0 1 0'
            elif axis.lower() == 'x':
                axis = '1 0 0'
            elif len(axis.split(',')) == 3:
                axis = np.array([float(q) for q in axis.split(',')])
                check_if_convertible(axis[0], float, 'axis (x-component)')
                check_if_convertible(axis[1], float, 'axis (y-component)')
                check_if_convertible(axis[2], float, 'axis (z-component)')
                axis = ' '.join(str(q) for q in axis/np.linalg.norm(axis))
            else:
                raise RuntimeError("The 'axis' keyword in fit_trajectory could not be understood")
            setups['ftr'] = add_once(sel_it, action)
            setups['ftr'] += add_once(geom_center, action)
            setups['ftr'] += add_once(mevsvd, action)
            setups['ftr'] += add_once(calc_principalaxes, action)
            setups['ftr'] += set_orientation(invert)
        setups['ftr'] += fit_slow(sel, axis)
        setups['ftr'] += add_once(scale_fit, action)
        if action.framenum == 0:
            curr = action.scene.actions.index(action)
            if any(['multiframe' in hl for ac in action.scene.actions[curr+1:] for x in ac.highlights.keys() for hl in
                    ac.highlights[x]]) or any(['animate' in ac.action_type for ac in action.scene.actions[curr+1:]]):
                fit_all = 1
            else:
                fit_all = 0
            setups['ftr'] += "fit_slow 1.0 {} {}\n".format(fit_all, mols)
    if 'rotate' in action.action_type:
        if action.framenum == 0:
            angle = action.parameters['angle']
            check_if_convertible(angle, float, 'angle')
            axis = action.parameters['axis']
            try:
                frac = action.parameters['fraction']
            except KeyError:
                pass
            else:
                check_if_convertible(frac, float, 'fraction')
                angle *= float(frac)
            if axis.lower() not in 'xyz':
                raise RuntimeError("'axis' must be either 'x', 'y' or 'z', {} was given instead".format(axis))
            setups['rot'] = 'rotate {} by {}\n'.format(axis.lower(), angle)
    if 'translate' in action.action_type:
        if action.framenum == 0:
            try:
                vec = action.parameters['vector'].split(',')
            except KeyError:
                raise RuntimeError("'translate' requires a specification of 'by' "
                                   "as three comma-separated vector components")
            check_if_convertible(vec[0], float, 'by (x-component)')
            check_if_convertible(vec[1], float, 'by (y-component)')
            check_if_convertible(vec[2], float, 'by (z-component)')
            try:
                frac = action.parameters['fraction']
            except KeyError:
                pass
            else:
                check_if_convertible(frac, float, 'fraction')
                vec = [str(frac*float(x)) for x in vec]
            setups['tns'] = 'translate by {}\n'.format(' '.join(vec))
    if 'zoom_in' in action.action_type or 'zoom_out' in action.action_type:
        if action.framenum == 0:
            scale = action.parameters['scale']
            check_if_convertible(scale, float, 'scale')
            prefix = 'zin' if 'zoom_in' in action.action_type else 'zou'
            scale = scale if 'zoom_in' in action.action_type else str(1/float(scale))
            setups[prefix] = 'scale by {}\n'.format(scale)
    if 'make_transparent' in action.action_type or 'make_opaque' in action.action_type:
        if action.framenum == 0:
            for t_ch in action.transp_changes.keys():
                material = action.transp_changes[t_ch]['material']
                try:
                    material = materials[material]
                except KeyError:
                    pass
                try:
                    opa = action.parameters['limit']
                except KeyError:
                    try:
                        opa = action.parameters['start']
                    except KeyError:
                        opa = 0 if 'transparent' in t_ch else 1
                    else:
                        opa = 1-opa if 'transparent' in t_ch else opa
                else:
                    opa = 1 - opa if 'transparent' in t_ch else opa
                check_if_convertible(opa, float, 'start/limit')
                opa = float(opa)
                setups[t_ch] = "material change opacity {} {}\n".format(material, opa)
    if 'animate' in action.action_type:
        setups['ani'] = ''
        try:
            smooth = action.parameters['smooth']
        except KeyError:
            pass
        else:
            check_if_convertible(smooth, int, 'smooth')
            setups['ani'] += 'set mtop [molinfo top]\nset nrep [molinfo $mtop get numreps]\n' \
                             'for {{set i 0}} {{$i < $nrep}} {{incr i}} {{\n' \
                             'mol smoothrep $mtop $i {}\n}}\n'.format(smooth)
        if action.framenum == 0:
            try:
                fr = action.parameters['frames']
            except KeyError:
                raise RuntimeError("With 'animate' the 'frames' parameter should also be specified")
            else:
                fr = fr.split(':')[-1]
                check_if_convertible(fr, int, 'frame')
                setups['ani'] += 'animate goto {}\n'.format(int(fr))
    if 'toggle_molecule' in action.action_type:
        setups['tog'] = ''
        try:
            molid = action.parameters['molecule_id']
        except KeyError:
            raise RuntimeError("With 'toggle_molecule', 'molecule_id' has to be specified")
        else:
            check_if_convertible(molid, int, 'molecule_id')
        try:
            top = True if action.parameters['top'].lower() in ['t', 'y', 'true', 'yes'] else False
        except KeyError:
            top = None
        try:
            active = True if action.parameters['active'].lower() in ['t', 'y', 'true', 'yes'] else False
        except KeyError:
            active = None
        try:
            freeze = True if action.parameters['freeze'].lower() in ['t', 'y', 'true', 'yes'] else False
        except KeyError:
            freeze = None
        try:
            drawn = True if action.parameters['drawn'].lower() in ['t', 'y', 'true', 'yes'] else False
        except KeyError:
            drawn = None
        if top:
            setups['tog'] += 'mol top {}'.format(molid)
        if active is not None:
            if active:
                setups['tog'] += 'mol active {}'.format(molid)
            else:
                setups['tog'] += 'mol inactive {}'.format(molid)
        if freeze is not None:
            if freeze:
                setups['tog'] += 'mol fix {}'.format(molid)
            else:
                setups['tog'] += 'mol free {}'.format(molid)
        if drawn is not None:
            if drawn:
                setups['tog'] += 'mol on {}'.format(molid)
            else:
                setups['tog'] += 'mol off {}'.format(molid)
    return setups


def gen_iterators(action):
    """
    to serve both Action and SimultaneousAction, we return
    a dictionary with three-letter labels and a list of
    values already formatted as a string
    :param action: Action or SimultaneousAction, object to extract info from
    :return: dict, formatted as label: iterator
    """
    iterators = OrderedDict()  # TODO support fractions in instantaneous actions
    num_precision = 5
    if action.framenum == 0:
        return iterators
    sigmoid, sls, abruptness = check_sigmoid(action.parameters)
    if 'rotate' in action.action_type:
        for rkey in sorted(list(action.rots.keys()), key=lambda x: int(x[3:])):
            angle = action.rots[rkey]['angle']
            check_if_convertible(angle, float, 'smooth')
            framenum, first, last = get_fraction(action, action.rots[rkey])
            if sigmoid:
                arr = sigmoid_norm_sum(float(angle), framenum, abruptness)[first:last]
            elif sls:
                arr = sigmoid_norm_sum_linear_mid(float(angle), framenum, abruptness)[first:last]
            else:
                arr = (np.ones(action.framenum) * float(angle)/framenum)[first:last]
            iterators[rkey] = ' '.join([str(round(el, num_precision)) for el in arr])
    if 'translate' in action.action_type:
        framenum, first, last = get_fraction(action, action.transl['translate'])
        if sigmoid:
            arr = sigmoid_norm_sum(1, framenum, abruptness)[first:last]
        elif sls:
            arr = sigmoid_norm_sum_linear_mid(1, framenum, abruptness)[first:last]
        else:
            arr = (np.ones(framenum)/framenum)[first:last]
        iterators['tns'] = ' '.join([str(round(el, num_precision)) for el in arr])
    if 'zoom_in' in action.action_type:
        scale = action.parameters['scale']
        check_if_convertible(scale, float, 'scale')
        framenum, first, last = get_fraction(action, action.zoom[list(action.zoom.keys())[0]])
        if sigmoid:
            arr = sigmoid_norm_prod(float(scale), framenum, abruptness)[first:last]
        else:
            arr = (np.ones(framenum) * float(scale)**(1/framenum))[first:last]
        iterators['zin'] = ' '.join([str(round(el, num_precision)) for el in arr])
    if 'zoom_out' in action.action_type:
        scale = action.parameters['scale']
        check_if_convertible(scale, float, 'scale')
        framenum, first, last = get_fraction(action, action.zoom[list(action.zoom.keys())[0]])
        if sigmoid:
            arr = sigmoid_norm_prod(1/float(scale), framenum, abruptness)[first:last]
        else:
            arr = (np.ones(framenum) * 1/(float(scale)**(1/framenum)))[first:last]
        iterators['zou'] = ' '.join([str(round(el, num_precision)) for el in arr])
    if 'fit_trajectory' in action.action_type:
        if sigmoid:
            arr = sigmoid_increments(action.framenum, abruptness)
        else:
            arr = np.ones(action.framenum)/action.framenum
        carr = np.cumsum(arr)[::-1]
        arr /= carr
        iterators['ftr'] = ' '.join([str(round(el, num_precision)) for el in arr])
    if 'make_transparent' in action.action_type or 'make_opaque' in action.action_type:
        for t_ch in action.transp_changes.keys():
            try:
                until = action.transp_changes[t_ch]['limit']
            except KeyError:
                until = 0 if 'transparent' in t_ch else 1
            else:
                check_if_convertible(until, float, 'limit')
                until = float(until)
            try:
                start = action.transp_changes[t_ch]['start']
            except KeyError:
                start = 1 if 'transparent' in t_ch else 0
            else:
                check_if_convertible(start, float, 'start')
                start = float(start)
            sigmoid, sls, abruptness = check_sigmoid(action.transp_changes[t_ch])
            framenum, first, last = get_fraction(action, action.parameters)
            if sigmoid:
                if 'transparent' in t_ch:
                    arr = (start - np.cumsum(sigmoid_norm_sum(start-until, framenum, abruptness)))[first:last]
                else:
                    arr = (start + np.cumsum(sigmoid_norm_sum(until-start, framenum, abruptness)))[first:last]
            else:
                arr = np.linspace(start, until, framenum)[first:last]
            iterators[t_ch] = ' '.join([str(round(el, num_precision)) for el in arr])
    if 'animate' in action.action_type:
        animation_frames = [x for x in action.parameters['frames'].split(':')]
        for val in animation_frames:
            check_if_convertible(val, int, 'frames')
        arr = np.linspace(int(animation_frames[0]), int(animation_frames[1]), action.framenum).astype(int)
        iterators['ani'] = ' '.join([str(int(el)) for el in arr])
    if 'highlight' in action.action_type:
        hls = [action.highlights[x] for x in action.highlights.keys()]
        hl_labels = list(action.highlights.keys())
        for lb, hl in zip(hl_labels, hls):
            try:
                fadein = hl['fade_in']
            except KeyError:
                fadein = 0.2
            else:
                check_if_convertible(fadein, float, 'fade_in')
            try:
                fadeout = hl['fade_out']
            except KeyError:
                fadeout = 0.2
            else:
                check_if_convertible(fadeout, float, 'fade_out')
            try:
                mframe = hl['multiframe']
            except KeyError:
                pass
            else:
                if ':' in mframe:
                    if mframe.count(':') != 1:
                        raise RuntimeError("In highlight's 'multiframe', only one colon (:) can be used")
                    mfr_init, mfr_end = mframe.split(':')
                    if mfr_init.count('-') == 2 or mfr_end.count('-') == 2:
                        if mfr_init.count('-') != 2 or mfr_end.count('-') != 2 \
                                or mfr_init.split('-')[-1] != mfr_end.split('-')[-1]:
                            raise RuntimeError("When using strides in highlight's 'multiframe', use them consistently "
                                               "(e.g. 1-20-2:4-50-2)")
                        mfr_split = ':' + mfr_end.split('-')[-1]
                    elif mfr_init.count('-') < 2 and mfr_end.count('-') < 2:
                        mfr_split = '1'
                    else:
                        raise RuntimeError("For highlight's multiframe, the format is beg1-end1-stride1:beg2-end2-"
                                           "stride2 (with strides and ends being optional), check your dashes")
                    if '-' in mfr_init:
                        mfr_00 = mfr_init.split('-')[0]
                        mfr_01 = mfr_init.split('-')[1]
                    else:
                        mfr_00 = mfr_01 = mfr_init
                    if '-' in mfr_end:
                        mfr_10 = mfr_end.split('-')[0]
                        mfr_11 = mfr_end.split('-')[1]
                    else:
                        mfr_10 = mfr_11 = mfr_end
                    iterators['mfr{}a'.format(lb)] = ' '.join([str(int(round(x, 0))) for x in
                                                               np.linspace(int(mfr_00), int(mfr_01), action.framenum)])
                    iterators['mfr{}b'.format(lb)] = ' '.join([str(int(round(x, 0))) for x in
                                                               np.linspace(int(mfr_10), int(mfr_11), action.framenum)])
                    iterators['mfr{}c'.format(lb)] = ' '.join([mfr_split for _ in range(action.framenum)])
            try:
                mode = hl['mode']
            except KeyError:
                hls = find_highlights_with_alias(action, hl)
                hls_upto = [h for h in hls[:hls.index(hl)]] if hls else False
                if hls_upto:
                    mode = 'n'
                else:
                    mode = 'ud'
            fadein, fadeout = float(fadein), float(fadeout)
            if fadein > 1 or fadeout > 1 or (mode == 'ud' and fadein + fadeout > 1):
                print('fade-in and fade-out fractions cannot sum to more than 1, will be rescaled')
                fadein = 1.0 if fadein > 1 else fadein
                fadeout = 1.0 if fadeout > 1 else fadeout
                if mode == 'ud' and fadein + fadeout > 1:
                    excess = (fadein + fadeout) - 1
                    fadein -= excess/2
                    fadeout -= excess/2
            frames_in = int(float(fadein) * action.framenum)
            frames_out = int(float(fadeout) * action.framenum)
            if mode != 'n' and 'alpha' in hl.keys() and ':' in hl['alpha']:
                raise RuntimeError('alphas can only be specified as ranges (x:y) when mode=n')
            if mode != 'd':
                try:
                    alpha = float(hl['alpha']) if 'alpha' in hl.keys() else 1
                except ValueError:
                    alpha = 1
            else:
                hls = find_highlights_with_alias(action, hl)
                hls = [h for h in hls[:hls.index(hl)] if 'alpha' in h.keys()]
                if hls and 'alpha' in hls[-1].keys():
                    last_alpha = hls[-1]['alpha'].split(':')[-1]
                else:
                    last_alpha = 1.0
                alpha = float(hl['alpha']) if 'alpha' in hl.keys() else float(last_alpha)
            arr = None
            if mode == 'u':
                arr_init = np.cumsum(sigmoid_norm_sum(alpha, frames_in, abruptness))
                arr = np.concatenate((arr_init, alpha*np.ones(action.framenum - frames_in)))
            elif mode == 'd':
                arr_term = alpha - np.cumsum(sigmoid_norm_sum(alpha, frames_out, abruptness))
                arr = np.concatenate((alpha*np.ones(action.framenum - frames_out), arr_term))
            elif mode == 'ud':
                arr_init = np.cumsum(sigmoid_norm_sum(alpha, frames_in, abruptness))
                arr_term = np.cumsum(sigmoid_norm_sum(alpha, frames_out, abruptness))
                arr = np.concatenate((arr_init, np.ones(action.framenum-frames_in-frames_out)*alpha, alpha-arr_term))
            elif mode == 'n':
                if 'alpha' in hl.keys():
                    if ':' in hl['alpha']:
                        al0 = float(hl['alpha'].split(':')[0])
                        al1 = float(hl['alpha'].split(':')[1])
                        arr_trans = np.cumsum(sigmoid_norm_sum(al1-al0, frames_in, abruptness))
                        arr = np.concatenate((al0 + arr_trans, np.ones(action.framenum-frames_in)*al1))
                    else:
                        arr = np.ones(action.framenum) * alpha
            else:
                raise RuntimeError('"mode" should be "u", "d", "n" or "ud"')
            if arr is not None:
                iterators['alp{}'.format(lb)] = ' '.join([str(round(el, num_precision)) for el in arr])
            if 'isovalue' in hl.keys() and ':' in hl['isovalue']:
                start_iso = float(hl['isovalue'].split(':')[0])
                end_iso = float(hl['isovalue'].split(':')[1])
                isoarr = start_iso + np.cumsum(sigmoid_norm_sum(end_iso - start_iso, action.framenum, abruptness))
                iterators['iso{}'.format(lb)] = ' '.join([str(round(el, num_precision)) for el in isoarr])
            if 'thickness' in hl.keys() and ':' in hl['thickness'] and mode == 'n':
                start_thi = float(hl['thickness'].split(':')[0])
                end_thi = float(hl['thickness'].split(':')[1])
                thiarr = start_thi + np.cumsum(sigmoid_norm_sum(end_thi - start_thi, action.framenum, abruptness))
                iterators['thi{}'.format(lb)] = ' '.join([str(round(el, num_precision)) for el in thiarr])
    return iterators


def gen_command(action):
    """
    We assume action_type is either a list of strings
    or a single string, so that one does not need to care
    whether we're dealing with a single action or many;
    we return a dict formatted consistently with gen_iterators()
    :param action: either Action or SimultaneousAction
    :return: dict, formatted as label: TCL command
    """
    commands = OrderedDict()
    materials = materials_dict()
    if action.framenum == 0:
        return commands
    if 'rotate' in action.action_type:
        for rkey in action.rots.keys():
            axis = action.rots[rkey]['axis']
            if axis.lower() not in 'xyz':
                raise RuntimeError("'axis' must be either 'x', 'y' or 'z', {} was given instead".format(axis))
            commands[rkey] = "set t [lindex ${} $i]\n" \
                             "  rotate {} by $t\n".format(rkey, axis.lower())
    if 'translate' in action.action_type:
        vec = action.parameters['vector'].split(',')
        commands['tns'] = "set tx [expr {} * [lindex $tns $i]]\n" \
                          "set ty [expr {} * [lindex $tns $i]]\n" \
                          "set tz [expr {} * [lindex $tns $i]]\n" \
                          "translate by $tx $ty $tz\n".format(*vec)
    if 'make_transparent' in action.action_type or 'make_opaque' in action.action_type:
        for t_ch in action.transp_changes.keys():
            material = action.transp_changes[t_ch]['material']
            try:
                material = materials[material]
            except KeyError:
                pass
            commands[t_ch] = "set t [lindex ${} $i]\n" \
                             "  material change opacity {} $t\n".format(t_ch, material)
    if 'zoom_in' in action.action_type:
        commands['zin'] = "set t [lindex $zin $i]\n" \
                          "  scale by $t\n"
    elif 'zoom_out' in action.action_type:
        commands['zou'] = "set t [lindex $zou $i]\n" \
                          "  scale by $t\n"
    if 'animate' in action.action_type:
        commands['ani'] = "set t [lindex $ani $i]\n" \
                          "  animate goto $t\n"
    if 'fit_trajectory' in action.action_type:
        mols = process_mols(action)
        if any(['multiframe' in hl for ac in action.scene.actions for x in ac.highlights.keys()
                for hl in ac.highlights[x]]):
            fit_all_frames = '1'
        else:
            fit_all_frames = '0'
        commands['ftr'] = "set t [lindex $ftr $i]\n" \
                          "  fit_slow $t {} {}\n".format(fit_all_frames, mols)
    if 'highlight' in action.action_type:
        hls = [action.highlights[x] for x in action.highlights.keys()]
        hl_labels = list(action.highlights.keys())
        for lb, hl in zip(hl_labels, hls):
            try:
                mode = hl['mode']
            except KeyError:
                hls = find_highlights_with_alias(action, hl)
                hls_upto = [h for h in hls[:hls.index(hl)]] if hls else False
                if hls_upto:
                    mode = 'n'  # TODO raise error when 'n' is not used with an alias
                else:
                    mode = 'ud'
            if mode == 'd':
                if not find_highlights_with_alias(action, hl):
                    raise RuntimeError('When mode=d, an alias has to be supplied to specify which highlight'
                                       'has to be turned off.')
            if not (mode == 'n' and 'alpha' not in hl.keys()):
                commands[lb] = "set t [lindex $alp{} $i]\n" \
                               "  material change opacity $mat{} $t\n".format(lb, lb)
            if 'multiframe' in hl.keys():
                if ':' not in hl['multiframe']:
                    mfr = hl['multiframe']
                    if mfr == 'now':
                        mframes = mfr
                    elif mfr.count('-') == 1:
                        mframes = ' '.join([str(x) for x in range(int(mfr.split('-')[0]), int(mfr.split('-')[1]) + 1)])

                    elif mfr.count('-') == 2:
                        mframes = ' '.join([str(x) for x in range(int(mfr.split('-')[0]), int(mfr.split('-')[1]) + 1,
                                                                  int(mfr.split('-')[2]))])
                    else:
                        raise RuntimeError("Malformed argument for highlight's 'multiframe': {}".format(mfr))
                    commands['mfr{}'.format(lb)] = 'mol drawframes top [lindex $repnums $repnum_{}] ' \
                                                   '{{{}}}'.format(lb, mframes)
                if hl['multiframe'] != 'now':
                    commands['mfr{}'.format(lb)] = 'set t [lindex $mfr{l}a $i]\n  set u [lindex $mfr{l}b $i]\n  ' \
                                                   'set v [lindex $mfr{l}c $i]\n  set frlist {{}}\n  for {{set j $t}}' \
                                                   ' {{$j <= $u}} {{incr j $v}} {{lappend frlist $j}}\n  mol draw' \
                                                   'frames top [lindex $repnums $repnum_{l}] $frlist\n'.format(l=lb)
            if 'isovalue' in hl.keys() and ':' in hl['isovalue']:
                commands['iso{}'.format(lb)] = 'set t [lindex $iso{} $i]\n' \
                                               '  mol modstyle [lindex $repnums $repnum_{}] top Isosurface $t 0 0 0 ' \
                                               '1 1\n'.format(lb, lb)
            if 'thickness' in hl.keys() and ':' in hl['thickness'] and mode == 'n' and 'alias' in hl.keys():
                hls = find_highlights_with_alias(action, hl)
                hls = [h for h in hls if 'style' in h.keys()]
                style = hls[0]['style'] if hls else 'newcartoon'
                if style == 'surf':
                    print('Variable thickness not supported for style=surf, skipping')
                    continue
                style_params = {'newcartoon': ['NewCartoon [expr {{0.32*', '30 4.1 0'],
                                'quicksurf': ['QuickSurf 0.9 [expr {{1.3/', '0.5 3.0'],
                                'licorice': ['Licorice [expr {{0.31*', '12.0 12.0'],
                                'vdw': ['VDW [expr {{1.05*', '20.0'],
                                'tube': ['Tube [expr {{0.40*', '20.0']}
                commands['thi{}'.format(lb)] = 'set t [lindex $thi{} $i]\n' \
                                               '  mol modstyle [lindex $repnums $repnum_{}] top {} $t}}] {} ' \
                                               '\n'.format(lb, lb, *style_params[style]).replace('{{', '{')
    return commands


def gen_cleanup(action):
    """
    Whenever a TCL action requires some
    post-execution cleanup (e.g. deletion
    of highlights), this fn generates code
    to handle this
    :param action: either Action or SimultaneousAction
    :return: dict, formatted as label: TCL command
    """
    cleanups = OrderedDict()
    if 'fit_trajectory' in action.action_type:
        flag = False
        current = action.scene.actions.index(action)
        for ac in action.scene.actions[current+1:]:
            if 'animate' in ac.action_type:
                flag = True
        if flag:
            mols = process_mols(action)
            cleanups['ftr'] = fit_slow(action.parameters['selection'], None)
            cleanups['ftr'] += "fit_slow 1 1 {}\n\n".format(mols)
    if 'highlight' in action.action_type:
        hls = [action.highlights[x] for x in action.highlights.keys()]
        hl_labels = list(action.highlights.keys())
        for lb, hl in zip(hl_labels, hls):
            try:
                mode = hl['mode']
            except KeyError:
                hls = find_highlights_with_alias(action, hl)
                hls_upto = [h for h in hls[:hls.index(hl)]] if hls else False
                if hls_upto:
                    mode = 'n'
                else:
                    mode = 'ud'
            if mode in ['ud', 'd']:
                cleanups[lb] = add_once(renumber_addedreps, action)
                cleanups[lb] += 'mol delrep [lindex $repnums $repnum_{}] top\n' \
                                'set repnums [renumber_addedreps $repnum_{} ' \
                                '$repnums]\n'.format(lb, lb)
    return cleanups


def check_if_convertible(string, object_type, param_name):
    """
    Checks if the user-specified value can be converted
    to the desired data type
    :param string: user-specified value
    :param object_type: what type should 'string' be convertible to
    :param param_name: name of the parameter in question
    :return: None
    """
    try:
        _ = object_type(string)
    except ValueError:
        raise RuntimeError("'{}' must be {}, instead '{}' was given".format(param_name, object_type, string))


def check_sigmoid(params_dict):
    """
    Checks sigmoid settings, for most actions
    this can be true, false or sls; in principle,
    transition abruptness can also be specified
    separately
    :param params_dict: a dict that will contain sigmoid parameters
    :return: bool, whether the transition follows a sigmoid
             bool, whether to make the transition sls (sigmoid-linear-sigmoid)
             float, abruptness of the transition (how steep is the sigmoid)
    """
    try:
        sigmoid = params_dict['sigmoid']
        sls = True if sigmoid.lower() == 'sls' else False  # sls stands for smooth-linear-smooth
        sigmoid = True if sigmoid.lower() in ['true', 't', 'y', 'yes'] else False
    except KeyError:
        sigmoid = True
        sls = False
    try:
        abruptness = float(params_dict['abruptness'])
    except KeyError:
        abruptness = 1
    else:
        check_if_convertible(abruptness, float, 'abruptness')
    return sigmoid, sls, abruptness


def get_fraction(action, action_dict):
    """
    When user only wants to run a fraction
    of the Action (e.g. to split one long Action
    between several shorter ones), this fn
    will calculate all numerical parameters
    :param action: either Action or SimultaneousAction
    :param action_dict: a dict that will contain fraction parameters
    :return: int, total number of frames (actual will be a fraction of this number)
             float, beginning of the action as numbered by framenum
             float, end of the action as numbered by framenum
    """
    try:
        frac = action_dict['fraction']
    except KeyError:
        first, last = None, None
        framenum = action.framenum
    else:
        frac = [x for x in frac.split(':')]
        frac[0] = float(frac[0]) if frac[0] else 0
        frac[1] = float(frac[1]) if frac[1] else 1
        framenum = int(action.framenum / (frac[1] - frac[0]))
        first, last = int(framenum * frac[0]), int(framenum * frac[1])
        diff = last - first
        last += action.framenum - diff
    return framenum, first, last


def find_highlights_with_alias(action, hl):
    hls = [act.highlights[h] for act in action.scene.actions for h in act.highlights
           if 'alias' in act.highlights[h].keys() and 'alias' in hl.keys()
           and act.highlights[h]['alias'] == hl['alias']]
    return hls


def process_mols(action):
    try:
        mols = action.parameters['molecules']
    except KeyError:
        mols = -2
    else:
        if mols == 'all':
            mols = -2
        elif mols == 'top':
            mols = -1
        else:
            mols = ' '.join(mols.split(','))
    return mols


def add_once(function, action):
    """
    Filters TCL functions to avoid multiple instances
    of exactly identical functions in the script
    (just for aesthetics, honestly)
    :param function: a Function object that returns the TCL code (see library below)
    :param action: either Action or SimultaneousAction
    :return: str, TCL code
    """
    if function not in action.scene.functions:
        action.scene.functions.append(function)
        return function()
    else:
        return ''
    
    
def materials_dict():
    return {'aochalky': 'AOChalky', 'aoedgy': 'AOEdgy', 'aoshiny': 'AOShiny',
            'blownglass': 'BlownGlass', 'brushedmetal': 'BrushedMetal', 'diffuse': 'Diffuse',
            'edgy': 'Edgy', 'edgyglass': 'EdgyGlass', 'edgyshiny': 'EdgyShiny', 'ghost': 'Ghost',
            'glass1': 'Glass1', 'glass2': 'Glass2', 'glass3': 'Glass3', 'glassbubble': 'GlassBubble',
            'glossy': 'Glossy', 'goodsell': 'Goodsell', 'hardplastic': 'HardPlastic',
            'metallicpastel': 'MetallicPastel', 'opaque': 'Opaque', 'rtchrome': 'RTChrome',
            'steel': 'Steel', 'translucent': 'Translucent', 'transparent': 'Transparent'}


def colors_dict():
    return {'blue': 0, 'red': 1, 'gray': 2, 'orange': 3, 'yellow': 4, 'tan': 5, 'silver': 6, 'green': 19,
            'white': 8, 'pink': 9, 'cyan': 10, 'purple': 11, 'lime': 12, 'mauve': 13, 'ochre': 14, 'iceblue': 15,
            'black': 16, 'violet': 25, 'magenta': 27, 'grey': 2}  # the default green is terrible

# ---------------------------- TCL function definitions ---------------------------- #


def reposition_dummies(sel1, sel2):
    code = 'proc reposition_dummies {{molind}} {{  animate dup $molind\n' \
           '  set sel [atomselect $molind "index 0"]\n  set ssel [atomselect top "{}"]\n' \
           '  $sel set {{x y z}} [list [geom_center $ssel]]\n  set ssel [atomselect top "{}"]\n' \
           '  set sel [atomselect $molind "index 1"]\n  $sel set {{x y z}} [list [geom_center $ssel]]\n' \
           '}}\n\n'.format(sel1, sel2)
    return code


def retr_vp():
    code = 'proc retr_vp {view_num} {\n  global viewpoints  \n  foreach mol [molinfo list] {\n' \
           '    molinfo $mol set rotate_matrix   $viewpoints($view_num,0,0)\n' \
           '    molinfo $mol set center_matrix   $viewpoints($view_num,0,1)\n' \
           '    molinfo $mol set scale_matrix   $viewpoints($view_num,0,2)\n' \
           '    molinfo $mol set global_matrix   $viewpoints($view_num,0,3)\n' \
           '  }\n' \
           '}\n\n'
    return code


def geom_center():
    code = 'proc geom_center {selection} {\n' \
           '    set gc [veczero]\n' \
           '    foreach coord [$selection get {x y z}] {\n' \
           '       set gc [vecadd $gc $coord]}\n' \
           '    return [vecscale [expr 1.0 /[$selection num]] $gc]}\n\n'
    return code


def fit_slow(selection, axis):
    if axis:
        extra = '    set temp_com [geom_center $fit_compare]\n' \
                '    $fit_system moveby [vecscale -1.0 $temp_com] \n' \
                '    set fit_matrix [set_orientation $fit_compare [list {}]]\n' \
                '    set scaled_fit [scale_fit $fit_matrix $frac]\n' \
                '    $fit_system move $scaled_fit\n' \
                '    $fit_system moveby $temp_com}}\n'.format(axis)
    else:
        extra = '    set fit_matrix [measure fit $fit_compare $fit_reference]\n' \
                '    set scaled_fit [scale_fit $fit_matrix $frac]\n' \
                '    $fit_system move $scaled_fit}}\n'.format()
    code = 'proc fit_slow {{frac {{calc_all 0}} {{top -1}}}} {{\n' \
           '  if {{$top == -1}} {{set topmol [molinfo top]; set listmol [list $topmol]}}' \
           '  elseif {{$top == -2}} {{set listmol [molinfo list]}}' \
           '  else {{set listmol [split $top]}}\n' \
           'foreach ml $listmol {{\n' \
           '  set curr_frame [molinfo $ml get frame]\n' \
           '  set fit_reference [atomselect $ml "{}" frame $curr_frame]\n' \
           '  set fit_compare [atomselect $ml "{}"]\n' \
           '  set fit_system [atomselect $ml "all"]\n' \
           '  set num_steps [molinfo $ml get numframes]\n' \
           '  set smooth_range [mol smoothrep $ml 0]\n' \
           '  if {{$calc_all == 0}} {{\n' \
           '    if {{$curr_frame > $smooth_range}} {{set start_step [expr $curr_frame - $smooth_range]}} ' \
           'else {{set start_step 0}}\n' \
           '    if {{$curr_frame < [expr $num_steps - $smooth_range]}} {{set last_step [expr $curr_frame + ' \
           '$smooth_range + 1]}} else {{set last_step $num_steps}}\n' \
           '  }}\\\n' \
           '  else {{\n' \
           '    set start_step 0\n' \
           '    set last_step $num_steps}}\n' \
           '  for {{set frame $start_step}} {{$frame < $last_step}} {{incr frame}} {{\n' \
           '    $fit_compare frame $frame\n' \
           '    $fit_system frame $frame\n' \
           '{} }} }}\n\n'.format(selection, selection, extra)
    return code


def scale_fit():
    code = 'proc scale_fit {fitting_matrix multip} {\n' \
           '  set pi 3.1415926535\n' \
           '  set R31 [lindex $fitting_matrix 2 0]\n' \
           '  if {$R31 == 1} {\n' \
           '    set phi1 0.\n' \
           '    set psi1 [expr atan2([lindex $fitting_matrix 0 1],[lindex $fitting_matrix 0 2]) ]\n' \
           '    set theta1 [expr -$pi/2]\n' \
           '  } elseif {$R31 == -1} {\n' \
           '    set phi1 0.\n' \
           '    set psi1 [expr atan2([lindex $fitting_matrix 0 1],[lindex $fitting_matrix 0 2]) ]\n' \
           '    set theta1 [expr $pi/2]\n' \
           '  } else {\n' \
           '    set theta1 [expr -asin($R31)]\n' \
           '    set cosT [expr cos($theta1)]\n' \
           '    set psi1 [expr  atan2([lindex $fitting_matrix 2 1]/$cosT,[lindex $fitting_matrix 2 2]/$cosT) ]\n' \
           '    set phi1 [expr  atan2([lindex $fitting_matrix 1 0]/$cosT,[lindex $fitting_matrix 0 0]/$cosT) ]\n' \
           '  }\n' \
           '  set theta [expr $multip*$theta1]\n' \
           '  set phi [expr $multip*$phi1]\n' \
           '  set psi [expr $multip*$psi1]\n' \
           '  lset fitting_matrix {0 0} [expr cos($theta)*cos($phi)]\n' \
           '  lset fitting_matrix {0 1} [expr sin($psi)*sin($theta)*cos($phi) - cos($psi)*sin($phi)]\n' \
           '  lset fitting_matrix {0 2} [expr cos($psi)*sin($theta)*cos($phi) + sin($psi)*sin($phi)]\n' \
           '  lset fitting_matrix {0 3} [expr $multip*[lindex $fitting_matrix 0 3]]\n' \
           '  lset fitting_matrix {1 0} [expr cos($theta)*sin($phi)]\n' \
           '  lset fitting_matrix {1 1} [expr sin($psi)*sin($theta)*sin($phi) + cos($psi)*cos($phi)]\n' \
           '  lset fitting_matrix {1 2} [expr cos($psi)*sin($theta)*sin($phi) - sin($psi)*cos($phi)]\n' \
           '  lset fitting_matrix {1 3} [expr $multip*[lindex $fitting_matrix 1 3]]\n' \
           '  lset fitting_matrix {2 0} [expr -sin($theta)]\n' \
           '  lset fitting_matrix {2 1} [expr sin($psi)*cos($theta)]\n' \
           '  lset fitting_matrix {2 2} [expr cos($psi)*cos($theta)]\n' \
           '  lset fitting_matrix {2 3} [expr $multip*[lindex $fitting_matrix 2 3]]\n' \
           '  return $fitting_matrix\n' \
           '}\n\n'
    return code


def sel_it():
    code = 'proc sel_it { sel COM} {\n' \
            '    set x [ $sel get x ]\n' \
            '    set y [ $sel get y ]\n' \
            '    set z [ $sel get z ]\n' \
            '    set Ixx 0\n' \
            '    set Ixy 0\n' \
            '    set Ixz 0\n' \
            '    set Iyy 0\n' \
            '    set Iyz 0\n' \
            '    set Izz 0\n' \
            '    foreach xx $x yy $y zz $z {\n' \
            '        set xx [expr $xx - [lindex $COM 0]]\n' \
            '        set yy [expr $yy - [lindex $COM 1]]\n' \
            '        set zz [expr $zz - [lindex $COM 2]]\n' \
            '        set Ixx [expr $Ixx + ($yy*$yy+$zz*$zz)]\n' \
            '        set Ixy [expr $Ixy - ($xx*$yy)]\n' \
            '        set Ixz [expr $Ixz - ($xx*$zz)]\n' \
            '        set Iyy [expr $Iyy + ($xx*$xx+$zz*$zz)]\n' \
            '        set Iyz [expr $Iyz - ($yy*$zz)]\n' \
            '        set Izz [expr $Izz + ($xx*$xx+$yy*$yy)]\n' \
            '    }\n' \
            '    return [list 2 3 3 $Ixx $Ixy $Ixz $Ixy $Iyy $Iyz $Ixz $Iyz $Izz]\n' \
            '}\n\n'
    return code


def calc_principalaxes():
    code = 'proc calc_principalaxes { sel } {\n' \
            '    set COM [geom_center $sel]\n' \
            '    set I [sel_it $sel $COM]\n' \
            '    set II [mevsvd_br $I]\n' \
            '    set eig_order [lsort -indices -real [lindex $II 1]]\n' \
            '    set a1 "[lindex $II 0 [expr 3 + [lindex $eig_order 0]]] [lindex $II 0 [expr 6 + ' \
           '[lindex $eig_order 0]]] [lindex $II 0 [expr 9 + [lindex $eig_order 0]]]"\n' \
            '    set a2 "[lindex $II 0 [expr 3 + [lindex $eig_order 1]]] [lindex $II 0 [expr 6 + ' \
           '[lindex $eig_order 1]]] [lindex $II 0 [expr 9 + [lindex $eig_order 1]]]"\n' \
            '    set a3 "[lindex $II 0 [expr 3 + [lindex $eig_order 2]]] [lindex $II 0 [expr 6 + ' \
           '[lindex $eig_order 2]]] [lindex $II 0 [expr 9 + [lindex $eig_order 2]]]"\n' \
            '    return [list $a1 $a2 $a3]\n' \
            '}\n\n'
    return code
    

def set_orientation(invert=False):
    inv = 'set old_axis {-1 -1 -1}\n\n' if invert else 'set old_axis {1 1 1}\n\n'
    code = '{}proc set_orientation {{ sel vector2 }} {{\n' \
           '    global old_axis\n' \
           '    set vector1 [lindex [calc_principalaxes $sel] 0]\n' \
           '    if {{[vecdot $vector1 $old_axis] < 0}} {{set vector1 [vecscale -1.0 $vector1]}}\n' \
           '    set old_axis $vector1\n' \
           '    set COM [geom_center $sel]\n' \
           '    set vec1 [vecnorm $vector1]\n' \
           '    set vec2 [vecnorm $vector2]\n' \
           '    set rotvec [veccross $vec1 $vec2]\n' \
           '    set sine   [veclength $rotvec]\n' \
           '    set cosine [vecdot $vec1 $vec2]\n' \
           '    set angle [expr atan2($sine,$cosine)]\n' \
           '    return [trans center $COM axis $rotvec $angle rad]\n' \
           '}}\n\n'.format(inv)
    return code


def mevsvd():
    code = 'proc mevsvd_br {A_in_out {eps 2.3e-16}} {\n' \
            '    set A $A_in_out\n' \
            '    set n [lindex $A 1]\n' \
            '    for {set i 0} {$i < $n} {incr i} {\n' \
            '        set ii [expr {3 + $i*$n + $i}]\n' \
            '        set v [lindex $A $ii]\n' \
            '        for {set j 0} {$j < $n} {incr j} {\n' \
            '            if { $i != $j } {\n' \
            '                set ij [expr {3 + $i*$n + $j}]\n' \
            '                set Aij [lindex $A $ij]\n' \
            '                set v [expr {$v - abs($Aij)}]\n' \
            '                }\n' \
            '             }\n' \
            '        if { ![info exists h] } { set h $v }\\\n' \
            '        elseif { $v < $h } { set h $v }\n' \
            '        }\n' \
            '    if { $h <= $eps } {\n' \
            '        set h [expr {$h - sqrt($eps)}]\n' \
            '        for {set i 0} {$i < $n} {incr i} {\n' \
            '            set ii [expr {3 + $i*$n + $i}]\n' \
            '            set Aii [lindex $A $ii]\n' \
            '            lset A $ii [expr {$Aii - $h}]\n' \
            '            }\n' \
            '        }\\\n' \
            '    else {\n' \
            '        set h 0.0\n' \
            '        }\n' \
            '    set count 0\n' \
            '  for {set isweep 0} {$isweep < 30 && $count < $n*($n-1)/2} {incr isweep} {\n' \
            '    set count 0   ;# count of rotations in a sweep\n' \
            '    for {set j 0} {$j < [expr {$n-1}]} {incr j} {\n' \
            '        for {set k [expr {$j+1}]} {$k < $n} {incr k} {\n' \
            '            set p [set q [set r 0.0]]\n' \
            '            for {set i 0} {$i < $n} {incr i} {\n' \
            '                set ij [expr {3+$i*$n+$j}]\n' \
            '                set ik [expr {3+$i*$n+$k}]\n' \
            '                set Aij [lindex $A $ij]\n' \
            '                set Aik [lindex $A $ik]\n' \
            '                set p [expr {$p + $Aij*$Aik}]\n' \
            '                set q [expr {$q + $Aij*$Aij}]\n' \
            '                set r [expr {$r + $Aik*$Aik}]\n' \
            '                }\n' \
            '             if { 1.0 >= 1.0 + abs($p/sqrt($q*$r)) } {\n' \
            '                 if { $q >= $r } {\n' \
            '                     incr count\n' \
            '                     continue\n' \
            '                     }\n' \
            '                 }\n' \
            '             set q [expr {$q-$r}]\n' \
            '             set v [expr {sqrt(4.0*$p*$p + $q*$q)}]\n' \
            '             if { $v == 0.0 } continue\n' \
            '             if { $q >= 0.0 } {\n' \
            '                 set c [expr {sqrt(($v+$q)/(2.0*$v))}]\n' \
            '                 set s [expr {$p/($v*$c)}]\n' \
            '                 }\\\n' \
            '             else {\n' \
            '                 set s [expr {sqrt(($v-$q)/(2.0*$v))}]\n' \
            '                 if { $p < 0.0 } { set s [expr {0.0-$s}] }\n' \
            '                 set c [expr {$p/($v*$s)}]\n' \
            '                 }\n' \
            '             for {set i 0} {$i < $n} {incr i} {\n' \
            '                set ij [expr {3+$i*$n+$j}]\n' \
            '                set ik [expr {3+$i*$n+$k}]\n' \
            '                set Aij [lindex $A $ij]\n' \
            '                set Aik [lindex $A $ik]\n' \
            '                lset A $ij [expr {$Aij*$c + $Aik*$s}]\n' \
            '                lset A $ik [expr {$Aik*$c - $Aij*$s}]\n' \
            '                }\n' \
            '            }\n' \
            '        } \n' \
            '    }\n' \
            '    set evals [list]\n' \
            '    for {set j 0} {$j < $n} {incr j} {\n' \
            '        set s 0.0\n' \
            '        set notpositive 0\n' \
            '        for {set i 0} {$i < $n} {incr i} {\n' \
            '            set ij [expr {3+$i*$n+$j}]\n' \
            '            set Aij [lindex $A $ij]\n' \
            '            if { $Aij <= 0.0 } { incr notpositive }\n' \
            '            set s [expr {$s + $Aij*$Aij}]\n' \
            '            }\n' \
            '        set s [expr {sqrt($s)}]\n' \
            '        if { $notpositive == $n } { set sf [expr {0.0-$s}] }\\\n' \
            '        else { set sf $s }\n' \
            '        for {set i 0} {$i < $n} {incr i} {\n' \
            '            set ij [expr {3+$i*$n+$j}]\n' \
            '            set Aij [lindex $A $ij]\n' \
            '            lset A $ij [expr {$Aij/$sf}]\n' \
            '            }\n' \
            '        lappend evals [expr {$s+$h}]\n' \
            '        }\n' \
            '     return [list $A $evals]\n' \
            '     }\n\n'
    return code


def renumber_addedreps():
    code = 'proc renumber_addedreps { deleted_num rnums } {\n' \
           '  for {set i 0} {$i < [llength $rnums]} {incr i} {\n' \
           '    if {$i >= $deleted_num} {lset rnums $i [expr [lindex $rnums $i] - 1]}\n' \
           '  }\n' \
           '  return $rnums\n' \
           '}\n\n'
    return code
