from lxml import etree

ns = {
    "mei": "http://www.music-encoding.org/ns/mei",
    "xml": "http://www.w3.org/XML/1998/namespace",
}

XML_ID = "{http://www.w3.org/XML/1998/namespace}id"


def add_sbs_every_n(
    active_dom: dict, context_doms: list, sbInterval: int, **addargs
):
    """
    Adds `<sb>` (system beginning) elements every n measures

    :param active_dom: dict containing {filename:Path/str?, dom:etree.Element}
    :type active_dom: dict
    :param context_doms: list containing dom dicts
    :type context_doms: list
    :param n: interval of system beginnings
    :type n: int
    :param addargs: Additional arguments that are unused
    """

    root = active_dom["dom"]

    measures = root.xpath(".//mei:measure", namespaces=ns)

    for count, measure in enumerate(measures):
        if (count + 1) % sbInterval == 0:
            sb = etree.Element("sb")
            parent = measure.getparent()
            parent.insert(parent.index(measure) + 1, sb)

    active_dom["dom"] = root
    output_message = ""

    return active_dom, output_message


def remove_all_sbs(active_dom: dict, context_doms: list, **addargs):
    """
    Removes all `<sb>`

    :param active_dom: dict containing {filename:Path/str?, dom:etree.Element}
    :type active_dom: dict
    :param context_doms: list containing dom dicts
    :type context_doms: list
    :param addargs: Additional arguments that are unused
    """

    root = active_dom["dom"]

    sbs = root.xpath(".//mei:sb", namespaces=ns)

    for sb in sbs:
        parent = sb.getparent()
        parent.remove(sb)

    active_dom["dom"] = root
    output_message = ""

    return active_dom, output_message


def change_octave(active_dom: dict, context_doms: list, addOctave: int, **addargs):
    """
    template function

    :param active_dom: dict containing {filename:Path/str?, dom:etree.Element}
    :type active_dom: dict
    :param context_doms: list containing dom dicts
    :type context_doms: list
    :param addOctave: integer by which octave will be raised
    :type addOctave: int
    :param addargs: Additional arguments that are unused
    """

    output_message = ""
    root = active_dom["dom"]

    # get all notes with @oct
    notes = root.xpath(".//mei:note[@oct]", namespaces=ns)

    for note in notes:
        # add add_octave to original value of @oct
        new_oct = int(note.get("oct")) + addOctave
        # check whether new oct value lies outside of SPN values, if so - skip
        if new_oct < 0 or new_oct > 9:
            output_message += (f"New octave value for note with xml:id '{note.get(XML_ID, 'unspecified')}' would be outside of SPN values - skipped.\n")
            continue
            # alternative, if program should stop:
            # raise RuntimeError("New octave value for note with xml:id '{note.get(XML_ID, 'unspecified')}' would be outside of SPN values - aborted.")
        note.set("oct", str(new_oct))

    active_dom["dom"] = root

    return active_dom, output_message


def _template_function(active_dom: dict, context_doms: list, **addargs):
    """
    template function

    :param active_dom: dict containing {filename:Path/str?, dom:etree.Element}
    :type active_dom: dict
    :param context_doms: list containing dom dicts
    :type context_doms: list
    :param addargs: Additional arguments that are unused
    """

    root = active_dom["dom"]

    # xpath_result = root.xpath(".//mei:elem[@attrib='value']", namespaces=ns)

    active_dom["dom"] = root
    output_message = ""

    return active_dom, output_message


def runtime_error(active_dom: dict, context_doms: list, **addargs):
    """
    This funtion raises a RuntimeError which will be shown to the user in mei-friend as they used a wrong iinput parameter or the wrong work package for the given file.

    :param active_dom: dict containing {filename:Path/str?, dom:etree.Element}
    :type active_dom: dict
    :param context_doms: list containing dom dicts
    :type context_doms: list
    :param addargs: Additional arguments that are unused
    """

    root = active_dom["dom"]

    # xpath_result = root.xpath(".//mei:elem[@attrib='value']", namespaces=ns)

    raise RuntimeError("This is a user error! It should be rendered")

    active_dom["dom"] = root
    output_message = ""

    return active_dom, output_message
