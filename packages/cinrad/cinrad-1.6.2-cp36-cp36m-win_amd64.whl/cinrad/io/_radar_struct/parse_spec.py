from glob import glob


def replace_dtype(s: str) -> str:
    s = s.replace("ulong", "u4")
    s = s.replace("ushort", "u2")
    s = s.replace("long", "i4")
    s = s.replace("short", "i2")
    return s.replace("\n", " ")


if __name__ == "__main__":
    spec_list = glob("*.spec")

    for fn in spec_list:
        f = open(fn, "r")
        content = f.read()
        f.close()
        sections = content.split("#")[1:]
        out = open(fn.replace("spec", "py"), "w")
        out.write("# Generated by parse_spec.py\n")
        out.write("# Do not modify\n")
        out.write("import numpy as np\n\n")
        for name, rawtype in zip(sections[0::2], sections[1::2]):
            content_r = replace_dtype(rawtype)
            content_list = content_r.split(" ")[1:]
            content_str = ['"{}"'.format(i) for i in content_list]
            dtype_list = [
                ", ".join((i, j)) for i, j in zip(content_str[0::2], content_str[1::2])
            ]
            ident_step = len(str("{} = [".format(name))) * " "
            out.write(
                "{} = [".format(name) + "({}),\n".format(dtype_list[0])
            )  # write first line
            for i in dtype_list[1:-1]:
                out.write(ident_step + "({}),\n".format(i))
            out.write(ident_step + "({})]\n\n".format(dtype_list[-1]))
            out.write("{}_dtype = np.dtype({})\n\n".format(name, name))
        out.close()
