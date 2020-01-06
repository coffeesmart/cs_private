def stats_analysis(file_path, figshow_onoff):
    import matplotlib.pyplot as plt
    import os
    from datetime import datetime

    def filetolist(filename):
        with open(filename, 'r') as f:
            f_list = list(f)

        return f_list

    def datasettocsv(list, filename, separator=','):
        f = open(filename, 'w')

        for l in list:
            line = ''
            for x in l:
                line = line + str(x) + separator
            line = line + '\n'
            f.write(line)
        f.flush()
        f.close()

    # dir = './'
    # stats_file_name = 'REFINE3D_2'
    #
    # stats_file = dir + stats_file_name

    raw = filetolist(file_path)
    file_name = (file_path.split('/'))[-1]
    file_dir = file_path.replace(file_name, "")

    now = datetime.now()
    nowDate = now.strftime('%Y%m%d_')

    save_path = file_dir + nowDate + file_name
    if os.path.isdir(save_path) == True :
        pass
    elif os.path.isdir(save_path) == False :
        os.mkdir(save_path)

    raw_split = []
    for ii in range(len(raw)):
        xx = raw[ii].split()
        if 'ITERATION' in xx:
            raw_split.append(xx)
        elif 'ORIENTATION' in xx and 'OVERLAP:' in xx:
            raw_split.append(xx)
        elif 'CORRELATION' in xx:
            raw_split.append(xx)
        elif 'SPECSCORE' in xx:
            raw_split.append(xx)
        else:
            pass

    raw_split2 = []
    for ii in range(len(raw_split)):
        yy = raw_split[ii]
        del yy[0]
        raw_split2.append(yy)

    if (len(raw_split2)) % 4 == 0:
        pass
    elif (len(raw_split2)) % 4 == 1:
        del raw_split2[len(raw_split2) - 1]
    elif (len(raw_split2)) % 4 == 2:
        del raw_split2[len(raw_split2) - 1]
        del raw_split2[len(raw_split2) - 1]
    elif (len(raw_split2)) % 4 == 3:
        del raw_split2[len(raw_split2) - 1]
        del raw_split2[len(raw_split2) - 1]
        del raw_split2[len(raw_split2) - 1]
    else:
        pass

    raw_split3 = []
    for ii in range(int(len(raw_split2) / 4)):
        raw_split3.append(raw_split2[4 * ii])
        zz = []
        zz.append(raw_split2[4 * ii + 1][0] + ' ' + raw_split2[4 * ii + 1][1])
        zz.append(raw_split2[4 * ii + 1][2])
        raw_split3.append(zz)

        zz2 = (raw_split2[4 * ii + 2][1]).split('/')
        zz_corr_AVG = [zz2[0], raw_split2[4 * ii + 2][2]]
        zz_corr_SDEV = [zz2[1], raw_split2[4 * ii + 2][3]]
        zz_corr_MIN = [zz2[2], raw_split2[4 * ii + 2][4]]
        zz_corr_MAX = [zz2[3], raw_split2[4 * ii + 2][5]]
        zz_corr = [raw_split2[4 * ii + 2][0], zz_corr_AVG, zz_corr_SDEV, zz_corr_MIN, zz_corr_MAX]
        raw_split3.append(zz_corr)

        zz3 = (raw_split2[4 * ii + 3][1]).split('/')
        zz_spec_AVG = [zz3[0], raw_split2[4 * ii + 3][2]]
        zz_spec_SDEV = [zz3[1], raw_split2[4 * ii + 3][3]]
        zz_spec_MIN = [zz3[2], raw_split2[4 * ii + 3][4]]
        zz_spec_MAX = [zz3[3], raw_split2[4 * ii + 3][5]]
        zz_spec = [raw_split2[4 * ii + 3][0], zz_spec_AVG, zz_spec_SDEV, zz_spec_MIN, zz_spec_MAX]
        raw_split3.append(zz_spec)

    gadget = []
    stats_list = []
    for ii in range(int(len(raw_split3) / 4)):
        gadget.append(raw_split3[4 * ii])
        gadget.append(raw_split3[4 * ii + 1])
        gadget.append(raw_split3[4 * ii + 2])
        gadget.append(raw_split3[4 * ii + 3])
        stats_list.append(gadget)
        gadget = []

    stats_iter = []
    stats_overlap = []
    stats_corr_AVG = []
    stats_corr_SDEV = []
    stats_corr_MIN = []
    stats_corr_MAX = []
    stats_spec_AVG = []
    stats_spec_SDEV = []
    stats_spec_MIN = []
    stats_spec_MAX = []
    for ii in range(len(stats_list)):
        stats_iter.append(float(stats_list[ii][0][1]))
        stats_overlap.append(float(stats_list[ii][1][1]))
        stats_corr_AVG.append(float(stats_list[ii][2][1][1]))
        stats_corr_SDEV.append(float(stats_list[ii][2][2][1]))
        stats_corr_MIN.append(float(stats_list[ii][2][3][1]))
        stats_corr_MAX.append(float(stats_list[ii][2][4][1]))
        stats_spec_AVG.append(float(stats_list[ii][3][1][1]))
        stats_spec_SDEV.append(float(stats_list[ii][3][2][1]))
        stats_spec_MIN.append(float(stats_list[ii][3][3][1]))
        stats_spec_MAX.append(float(stats_list[ii][3][4][1]))

    plt.figure(figsize=(15, 5))

    plt.subplot(131)
    plt.title('Orientation overlap')
    plt.xlabel('Iterations')
    plt.ylabel('Orientation overlap')
    plt.scatter(stats_iter, stats_overlap, s=3, color='red')
    plt.axhline(y=0.9, color='blue', linewidth=1, label='Overlap=0.9 line')
    plt.legend(loc='upper left', fontsize=7)
    plt.ylim((-0.05, 1.05))
    plt.xlim((-0.05, len(stats_list) + 0.05))

    plt.subplot(132)
    plt.title('Correlation')
    plt.xlabel('Iterations')
    plt.ylabel('Correlation')
    plt.scatter(stats_iter, stats_corr_AVG, s=3, color='red', label='AVG')
    plt.scatter(stats_iter, stats_corr_SDEV, s=3, color='blue', label='SDEV')
    plt.scatter(stats_iter, stats_corr_MIN, s=3, color='green', label='MIN')
    plt.scatter(stats_iter, stats_corr_MAX, s=3, color='grey', label='MAX')
    plt.legend(loc='upper left', fontsize=6)
    plt.ylim((-0.05, 1.05))
    plt.xlim((-0.05, len(stats_list) + 0.05))

    plt.subplot(133)
    plt.title('Specscore')
    plt.xlabel('Iterations')
    plt.ylabel('Specscore')
    plt.scatter(stats_iter, stats_spec_AVG, s=3, color='red', label='AVG')
    plt.scatter(stats_iter, stats_spec_SDEV, s=3, color='blue', label='SDEV')
    plt.scatter(stats_iter, stats_spec_MIN, s=3, color='green', label='MIN')
    plt.scatter(stats_iter, stats_spec_MAX, s=3, color='grey', label='MAX')
    plt.legend(loc='upper left', fontsize=6)
    plt.ylim((-0.05, 1.05))
    plt.xlim((-0.05, len(stats_list) + 0.05))

    plt.savefig(save_path + '/SIMPLE_stats_fig.png')

    if figshow_onoff == 'on' :
        plt.show()
        plt.clf()
    elif figshow_onoff == 'off' :
        pass

    stats_list_for_csv = []
    stats_list_for_csv.append(['ITERATION', 'ORIENTATION OVERLAP', 'CORRELATION', '', '', '', 'SPECSCORE', '', '', ''])
    stats_list_for_csv.append(['', '', 'AVG', 'SDEV', 'MIN', 'MAX', 'AVG', 'SDEV', 'MIN', 'MAX'])
    for ii in range(len(stats_list)):
        aa = stats_list[ii]
        for_csv_element = [aa[0][1], aa[1][1], aa[2][1][1], aa[2][2][1], aa[2][3][1], aa[2][4][1], aa[3][1][1],
                           aa[3][2][1], aa[3][3][1], aa[3][4][1]]
        stats_list_for_csv.append(for_csv_element)

    datasettocsv(stats_list_for_csv, save_path + '/stats_info.csv')

    return save_path

