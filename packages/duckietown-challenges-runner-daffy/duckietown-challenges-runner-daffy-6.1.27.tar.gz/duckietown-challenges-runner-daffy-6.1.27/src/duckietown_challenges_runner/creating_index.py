import os

from zuper_commons.fs import write_ustring_to_utf8_file

from duckietown_challenges import DEFAULT_DTSERVER


def create_index_files(wd, job_id):
    for root, dirnames, filenames in os.walk(wd, followlinks=True):
        # print(root, dirnames, filenames)
        index = os.path.join(root, "index.html")
        if not os.path.exists(index):
            d = create_index(root, dirnames, filenames, job_id)
            write_ustring_to_utf8_file(d, index)


def create_index(root, dirnames, filenames, job_id):
    s = "<html><head></head><body>\n"

    url = DEFAULT_DTSERVER + f"/humans/jobs/{job_id}"
    s += f'<p>These are the output for <a href="{url}">Job {job_id}</a>'
    s += "<table>"

    for d in dirnames:
        s += f'\n<tr><td></td><td><a href="{d}">{d}/</td></tr>'

    for f in filenames:
        size = os.stat(os.path.join(root, f)).st_size
        s += f'\n<tr><td>{size / (1024 * 1024.0):.3f} MB</td><td><a href="{f}">{f}</td></tr>'

    s += "\n</table>"
    s += "\n</body></head>"
    return s
