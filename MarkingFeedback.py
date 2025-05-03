"""
The path to the repository with comments should be specified in
MarkingFeedback.sublime-settings
"""

import sublime
import sublime_plugin

global sections, sections_list


class SectionAwareCompletions(sublime_plugin.EventListener):

    def __init__(self):
        global sections, sections_list

        # load dictionary
        settings = sublime.load_settings("MarkingFeedback.sublime-settings")
        dict_path = settings.get("repository_path", None)

        if not dict_path:
            raise Exception("Repository path not specified in MarkingFeedback.sublime-settings!")

        sections = {}
        current = None
        for l in open(dict_path):
            l = l.strip()
            if l.startswith("#"):
                sections[l] = []
                current = l
                continue
            alist = sections[current]
            alist.append(l)
            sections[current] = alist

        sections_list = list(sections.keys())

    def on_query_completions(self, view, prefix, locations):

        global sections, sections_list

        point = locations[0]

        # search backwards to find the first section heading
        matches = [view.find(x, start_pt=point, flags=8).end() for x in sections_list]

        # if no matches found, return empty list
        if max(matches) == -1:
            return []

        locs = [point - x for x in matches]
        selected_section = sections_list[locs.index(min(locs))]

        return sections[selected_section]

