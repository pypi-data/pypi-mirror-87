from rapidfuzz import fuzz
from pptx2md.global_var import g
import re
import os

class outputter(object):
    def __init__(self, file_path):
        os.makedirs(os.path.dirname(os.path.abspath(file_path)), exist_ok=True)
        self.ofile = open(file_path, 'w', encoding='utf8')
    def put_title(self, text, level):
        pass
    def put_list(self, text, level):
        pass
    def put_para(self, text):
        pass
    def put_image(self, path, width):
        pass
    def get_accent(self, text):
        pass
    def get_strong(self, text):
        pass
    def get_colored(self, text, rgb):
        pass
    def get_hyperlink(self, text, url):
        pass
    def get_escaped(self, text):
        pass
    def write(self, text):
        self.ofile.write(text)
    def flush(self):
        self.ofile.flush()
    def close(self):
        self.ofile.close()


class md_outputter(outputter):
    # write outputs to markdown
    def __init__(self, file_path):
        super().__init__(file_path)
        self.esc_re1 = re.compile(r'([\\\*`!_\{\}\[\]\(\)#\+-\.])')
        self.esc_re2 = re.compile(r'(<[^>]+>)')

    def put_title(self, text, level):
        text = text.strip()
        if not fuzz.ratio(text, g.last_title.get(level, ''), score_cutoff=92):
            self.ofile.write('#'*level + ' ' + text + '\n\n')
            g.last_title[level] = text

    def new_line(self):
        self.ofile.write('\n\n---\n\n')

    def put_list(self, text, level):
        self.ofile.write('  '*level + '* ' + text.strip() + '\n')
        
    def put_para(self, text):
        self.ofile.write(text + '\n\n')

    def put_image(self, path, width):
        self.ofile.write('<img src="%s" width=%spx />\n\n' % (path, width))
    
    def get_accent(self, text):
        return ' _' + text + '_ '
    
    def get_strong(self, text):
        return ' __' + text + '__ '

    def get_colored(self, text, rgb):
        return ' <span style="color:#%s">%s</span> ' % (str(rgb), text)

    def get_hyperlink(self, text, url):
        return '[' + text + '](' + url + ')'

    def esc_repl(self, match):
        return '\\' + match.group(0)

    def get_escaped(self, text):
        text = re.sub(self.esc_re1, self.esc_repl, text)
        text = re.sub(self.esc_re2, self.esc_repl, text)
        return text


class wiki_outputter(outputter):
    # write outputs to wikitext
    def __init__(self, file_path):
        super().__init__(file_path)
        self.esc_re = re.compile(r'<([^>]+)>')

    def put_title(self, text, level):
        text = text.strip()
        if not fuzz.ratio(text, g.last_title.get(level, ''), score_cutoff=92):
            self.ofile.write('!'*level + ' ' + text + '\n\n')
            g.last_title[level] = text

    def put_list(self, text, level):
        self.ofile.write('*'*(level+1) + ' ' + text.strip() + '\n')
        
    def put_para(self, text):
        self.ofile.write(text + '\n\n')

    def put_image(self, path, width):
        self.ofile.write('<img src="%s" width=%spx />\n\n' % (path, width))
    
    def get_accent(self, text):
        return ' __' + text + '__ '
    
    def get_strong(self, text):
        return ' \'\'' + text + '\'\' '

    def get_colored(self, text, rgb):
        return ' @@color:#%s; %s @@ ' % (str(rgb), text)

    def get_hyperlink(self, text, url):
        return '[[' + text + '|' + url + ']]'

    def esc_repl(self, match):
        return "''''" + match.group(0)

    def get_escaped(self, text):
        text = re.sub(self.esc_re, self.esc_repl, text)
        return text


class madoko_outputter(outputter):
    # write outputs to madoko markdown
    def __init__(self, file_path):
        super().__init__(file_path)
        self.ofile.write('[TOC]\n\n')
        self.esc_re1 = re.compile(r'([\\\*`!_\{\}\[\]\(\)#\+-\.])')
        self.esc_re2 = re.compile(r'(<[^>]+>)')

    def put_title(self, text, level):
        text = text.strip()
        if not fuzz.ratio(text, g.last_title.get(level, ''), score_cutoff=92):
            self.ofile.write('#'*level + ' ' + text + '\n\n')
            g.last_title[level] = text

    def new_line(self):
        self.ofile.write('\n---\n')

    def put_list(self, text, level):
        self.ofile.write('  '*level + '* ' + text.strip() + '\n')
        
    def put_para(self, text):
        self.ofile.write(text + '\n\n')

    def put_image(self, path, width):
        if width >= 500:
            self.ofile.write('~ Figure {caption: image caption}\n')
            self.ofile.write('![](%s){width:%spx;}\n' % (path, width))
            self.ofile.write('~\n\n')
        else:
            self.ofile.write('<img src="%s" width=%spx />\n\n' % (path, width))
    
    def get_accent(self, text):
        return ' _' + text + '_ '
    
    def get_strong(self, text):
        return ' __' + text + '__ '

    def get_colored(self, text, rgb):
        return ' <span style="color:#%s">%s</span> ' % (str(rgb), text)

    def get_hyperlink(self, text, url):
        return '[' + text + '](' + url + ')'

    def esc_repl(self, match):
        return '\\' + match.group(0)

    def get_escaped(self, text):
        text = re.sub(self.esc_re1, self.esc_repl, text)
        text = re.sub(self.esc_re2, self.esc_repl, text)
        return text
