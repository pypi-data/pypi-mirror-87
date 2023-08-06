__all__ = [
    "image_processing",
    "make_tex_document",
    "build_bbox",
]


def image_processing(param, analyse_morpho=True):

    # 3rd party import
    from pathlib import Path
    import pandas as pd
    
    # Inernal import
    from ./image_features_extract import read_image,gaussian_flattening
    from ./image_features_extract import xRemoveSpriesHorizontal, Otsu_tresholding

    # lecture de l'image
    im_brute, n_row, n_col = read_image(param["repertoire"] / param["file"])

    # mise à plat de l'image
    im_flat = gaussian_flattening(im_brute, param["sigma"])
    # im_flat = poly_flattening(im_brute)

    # supression des traces verticales
    im_corr_strie = xRemoveSpriesHorizontal(
        im_flat, param["decNum_h"], param["wname"], param["sigma_wl_h"]
    )

    # binarisation de l'image
    im_bin = Otsu_tresholding(im_corr_strie, Ostu_corr=param["Ostu_corr"])

    # analyse morphologique
    df = None
    if analyse_morpho:
        file_save_excel = Path(param["file"]).stem + ".xlsx"
        df = analyse_morphologique(im_bin)
        df.to_excel(param["dir_results"] / file_save_excel)
    return im_brute, im_corr_strie, im_flat, im_bin, df


def make_tex_document(
    param,
    im_brute,
    im_corr_strie,
    im_flat,
    im_bin,
    df,
    mode="w",
    flag=False,
    new_section=False,
):
    # 3rd party import
    import numpy as np
    import matplotlib.pyplot as plt
    import matplotlib
    from pathlib import Path
    import os

    size_min = 50
    alpha1 = 0.35
    alpha2 = 0.8

    print(param["file"])
    n_row, n_col = np.shape(im_brute)

    fig = plt.figure(figsize=(8, 8))
    ax1 = fig.add_subplot(111)
    im_flat = im_flat - im_flat.min()
    ax1.imshow(im_flat, interpolation="nearest", cmap=plt.cm.gray)

    df1 = df.query("size >= @size_min")
    patchesb = []
    for x1, y1, r in zip(df1["y"], df1["x"], df1["size"]):
        circle = plt.Circle((x1, y1), np.sqrt(r / np.pi))
        patchesb.append(circle)

    df1 = df.query("size < @size_min")
    patchesc = []
    for x1, y1, r in zip(df1["y"], df1["x"], df1["size"]):
        circle = plt.Circle((x1, y1), np.sqrt(r / np.pi))
        patchesc.append(circle)

    p = matplotlib.collections.PatchCollection(
        patchesb, cmap=matplotlib.cm.jet, alpha=alpha1, facecolor="blue"
    )
    pc = matplotlib.collections.PatchCollection(
        patchesc, cmap=matplotlib.cm.jet, alpha=alpha2, facecolor="green"
    )
    ax1.add_collection(p)
    ax1.add_collection(pc)
    file_save_im_brute = Path(param["file"]).stem + "-im-brute.jpg"
    plt.savefig(param["dir_results"] / file_save_im_brute, bbox_inches="tight")
    plt.close(fig)

    fig = plt.figure(figsize=(8, 8))
    ax1 = fig.add_subplot(111)
    ax1.imshow(convert(im_bin), interpolation="nearest", cmap=plt.cm.gray)
    file_save_im_bin = Path(param["file"]).stem + "-im-bin.jpg"
    plt.savefig(param["dir_results"] / file_save_im_bin, bbox_inches="tight")
    plt.close(fig)

    fig = plt.figure(figsize=(8, 8))
    ax1 = fig.add_subplot(111)
    ax1.hist(df["size"], bins=40)
    ax1.set_title("histogramme des tailles")
    file_save_im_hist = Path(param["file"]).stem + "-im-hist.jpg"
    plt.savefig(param["dir_results"] / file_save_im_hist, bbox_inches="tight")
    plt.close(fig)

    fig = plt.figure(figsize=(8, 8))
    ax1 = fig.add_subplot(111)
    ax1.boxplot(df["size"])
    file_save_im_erea = Path(param["file"]).stem + "-im-bbox.jpg"
    plt.savefig(param["dir_results"] / file_save_im_erea, bbox_inches="tight")
    plt.close(fig)

    file_save_doc_tex = Path(param["file"]).stem + "_doc_tex.tex"
    with open(param["dir_tex"] / Path("rapport.tex"), mode) as doc:
        if mode == "w":
            doc.write(
                r"""\documentclass[a4paper, 10pt]{article}
        \usepackage[american]{babel}
        \usepackage{amsmath}
        \usepackage{amsthm}
        \numberwithin{equation}{section}
        \usepackage[left=2cm,right=2cm,top=2cm,bottom=2cm]{geometry}
        \usepackage{graphicx}
        \usepackage{hyperref}
        \usepackage{empheq}
        \usepackage{pythonhighlight}"""
            )
            doc.write(
                r"\graphicspath{"
                + ",".join(
                    ["{./" + "wafer " + str(i) + "/" + "results}" for i in range(1, 6)]
                )
                + "}"
            )
            doc.write(
                r"""\begin{document}
        \tableofcontents
        \newpage"""
                + "\n"
            )
            # doc.write(r'\section{' + str(param['repertoire']).split('\\')[-2]+'}'+'\n')

            doc.write(r"\section{Parameters}")
            doc.write(
                r"\begin{center} \begin{tabular}{|" + " | ".join(["l"] * 2) + "|}\n"
            )
            doc.write("\\hline\n")
            doc.write(" & ".join([str(x) for x in ["parameter", "Value"]]) + " \\\\\n")
            doc.write("\\hline\n")
            doc.write("\\hline\n")
            for key, value in param.items():
                if key in ["wname", "sigma_wl_h", "decNum_h", "sigma", "Ostu_corr"]:

                    doc.write(key.replace("_", "\_") + " & " + str(value) + " \\\\\n")
                    doc.write("\\hline\n")
            doc.write(r"\end{tabular} \end{center} ")

            doc.write(r"\section{" + param["coupe"] + "}" + "\n")
        if new_section:
            doc.write(r"\subsection{" + param["wafer"] + "}" + "\n")
        doc.write(r"\subsubsection{" + param["file"] + "}" + "\n")
        doc.write(
            r"""\begin{figure}[h]
        \begin{center}
        \begin{tabular}{cc}
        (a) & (b)\\"""
            + "\n"
        )
        doc.write(
            r"\includegraphics[width=0.5\textwidth]{"
            + file_save_im_brute
            + r"} & \includegraphics[width=0.5\textwidth]{"
            + file_save_im_bin
            + r"}\\"
            + "\n"
        )
        doc.write(r"(c) & (d)\\" + "\n")
        doc.write(
            r"\includegraphics[width=0.5\textwidth]{"
            + file_save_im_hist
            + r"} & \includegraphics[width=0.5\textwidth]{"
            + file_save_im_erea
            + r"}\\"
            + "\n"
        )
        doc.write(
            r"""\end{tabular}
        \end{center}
        \caption{Image processing: (a) Superposition of the flattened image with the detected defaults, the erea of the circles
        are equal to the erea of the defaults, the green circle have an area less than 50 px, the blue one have area greater or
        equal than 50 px
        ; (b) Binarized image; (c) Area histogram; (d) Box plot of the area.}
        \end{figure}"""
            + "\n"
        )
        if flag:
            build_bbox(param, size_min=0)
            doc.write(r"\section {Synthese}")
            doc.write(
                r"\includegraphics[width=0.9\textwidth]{synthesege0.png} \newpage "
            )
            build_bbox(param, size_min=size_min, method="lt")
            doc.write(
                r"\includegraphics[width=0.9\textwidth]{syntheselt"
                + str(size_min)
                + r".png} \newpage "
            )
            build_bbox(param, size_min=size_min, method="ge")
            doc.write(
                r"\includegraphics[width=0.9\textwidth]{synthesege"
                + str(size_min)
                + ".png}"
            )
            doc.write(r"\end {document}")
        else:
            doc.write(r"\newpage")

    return


def build_bbox(param, size_min=50, method="ge"):

    # 3rd party import
    import pandas as pd
    from pathlib import Path

    REP = [
        param["root"] / Path(param["coupe"]) / Path("wafer " + str(i)) / Path("results")
        for i in range(1, 6)
    ]
    s = {}
    len_max = 0
    for rep in REP:
        for x in [y for y in os.listdir(rep) if y.split(".")[-1] == "xlsx"]:
            df = pd.read_excel(rep / x)
            key = x.split(".")[0]
            if method == "ge":
                s[key] = df.query("size >= @size_min")["size"]
            else:
                s[key] = df.query("size < @size_min")["size"]

            len_max = max(len(s[key]), len_max)
    for key, value in s.items():
        dif = len_max - len(value)
        if dif > 0:
            a = list(value)
            a.extend([None] * (dif))
            s[key] = a
    df = pd.DataFrame.from_dict(s)

    ax = df.plot.box(rot=0, figsize=(8, 15), grid=True, vert=False)
    ax.set_title(coupe)
    plt.savefig(
        param["root"]
        / Path(param["coupe"])
        / Path("synthese" + method + str(size_min) + ".png"),
        bbox_inches="tight",
    )
    plt.close(fig)
    return
