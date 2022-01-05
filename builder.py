import os
import sys
import yaml
import shutil
import argparse

from jinja2 import Environment
from jinja2 import FileSystemLoader

from markdown import markdown
from bs4 import BeautifulSoup

def get_args():

    args_parser = argparse.ArgumentParser()

    args_parser.add_argument(
        '--input',
        type = str,
        help = 'input directory with source data',
        required = True
    )

    args_parser.add_argument(
        '--output',
        type = str,
        help = 'output directory with result data',
        required = True
    )

    args_parser.add_argument(
        '--config',
        type = str,
        help = 'configuration file for builder',
        required = True
    )

    return args_parser.parse_args()

def get_paths():
    
    content_dirpath         = args.input
    content_pages_dirpath   = os.path.join(content_dirpath, 'pages')
    content_notes_dirpath   = os.path.join(content_pages_dirpath, 'notes')

    project_dirpath         = args.output
    project_notes_dirpath   = os.path.join(project_dirpath, 'notes')

    return {            

        'content_dirpath':          content_dirpath,
        'content_pages_dirpath':    content_pages_dirpath,
        'content_notes_dirpath':    content_notes_dirpath,

        'project_dirpath':          project_dirpath,
        'project_notes_dirpath':    project_notes_dirpath

    }

def get_config():

    config_filepath = args.config

    return read_yaml_file(config_filepath)

def clear_project():

    project_dirpath = paths.get('project_dirpath')

    for project_file in os.listdir(project_dirpath):

        protected_files = ['.git', 'CNAME']

        if project_file not in protected_files:

            project_file_path = os.path.join(project_dirpath, project_file)
            
            try:

                if os.path.isfile(project_file_path):
                    os.unlink(project_file_path)

                elif os.path.isdir(project_file_path):
                    shutil.rmtree(project_file_path)

            except Exception as e:
                print(e)

def build_project():

    def get_templates():

        templates_dirpath = os.path.join(BUILDER_DIRPATH, 'templates')

        return Environment(loader = FileSystemLoader(templates_dirpath))

    def get_language():

        filepath = os.path.join(paths['content_dirpath'], 'language.yaml')

        return read_yaml_file(filepath)

    def get_tags():

        filepath = os.path.join(paths['content_dirpath'], 'tags.yaml')

        return read_yaml_file(filepath)

    def get_pages():

        def get_page():

            def get_attachments():

                def is_attachment():

                    filepath = os.path.join(page_content_dirpath, file)
                    
                    is_file             = os.path.isfile(filepath)
                    is_not_predefined   = not file in predefined_files
                    
                    return is_file and is_not_predefined

                attachments         = []
                predefined_files    = ['index.md', 'index.yaml']

                files = os.listdir(page_content_dirpath)

                for file in files:
                
                    if is_attachment():
                        attachments.append(file)

                return attachments

            def get_path():

                path = page_content_dirpath
                dirs = []

                while path != paths['content_pages_dirpath']:
                    
                    splitted_path = os.path.split(path)

                    path = splitted_path[0]

                    dirs.append(splitted_path[1])

                dirs = list(reversed(dirs))

                if len(dirs) > 0:
                    result = '/' + '/'.join(dirs) + '/'
                else:
                    result = '/'

                return result
        
            def get_html():

                def replace_links_to_social_networks():

                    def replace_github_gist_link():

                        marker = 'https://gist.github.com/'
                        
                        if line.startswith(marker):

                            gist = line.strip().replace(marker, '').split('/')

                            gist_owner = gist[0]
                            gist_id    = gist[1]

                            template = '<script src="https://gist.github.com/{0}/{1}.js">{2}</script>'
                                                        
                            lines[index] = template.format(gist_owner, gist_id, language['gist'])

                    def replace_twitter_link():

                        marker = 'https://twitter.com/'

                        if line.startswith(marker):

                            tweet_url   = line.strip()
                            tweet_id    = tweet_url.split('/')[5]

                            template = '<div class="blog-embedded-tweet" data-tweet-id="{1}"><a href="{0}" class="link blue dim bb">' + language['tweet'] + '</a></div>'

                            lines[index] = template.format(tweet_url, tweet_id)

                    def replace_youtube_link(marker):

                        if line.startswith(marker):

                            video_id = line.strip().replace(marker, '')
                            template = '<iframe width="560" height="315" src="https://www.youtube.com/embed/{0}" frameborder="0" allow="accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>'

                            lines[index] = template.format(video_id)

                    lines = result.splitlines()

                    for (index, line) in enumerate(lines):

                        replace_twitter_link()
                        replace_github_gist_link()

                        replace_youtube_link('https://www.youtube.com/watch?v=')
                        replace_youtube_link('https://youtu.be/')                    

                    return '\n'.join(lines)

                def update_html():

                    def get_link(link):

                        result = link
                        is_url = link.startswith('http://') or link.startswith('https://')

                        if not is_url:
                            
                            prefix = config['url']

                            is_relative_path = not link.startswith('/')

                            if is_relative_path:
                                prefix = prefix + page['path']

                            result = prefix + link

                        return result

                    soup = BeautifulSoup(result, features = "html.parser")

                    for tag in soup.find_all("ol"):

                        tag['class'] = "measure-wide"

                    for tag in soup.find_all("ul"):

                        tag['class'] = "measure-wide"

                    for tag in soup.find_all("p"):

                        tag['class'] = "measure-wide"

                    for tag in soup.find_all("img"):

                        tag['src'] = get_link(tag['src'])

                    for tag in soup.find_all("a"):

                        tag['target'] = '_blank'

                        if tag.find('img') == None:                            
                            tag['class'] = "link blue dim bb"
                        
                        tag['href'] = get_link(tag['href'])

                    return str(soup)

                text_filepath = os.path.join(page_content_dirpath, 'index.md')

                with open(text_filepath, encoding = 'utf-8-sig') as handle:
                    result = handle.read()

                result = replace_links_to_social_networks()
                result = markdown(result)
        
                return update_html()

            def get_date():

                date    = page['metadata']['created']

                year    = str(date.year)
                month   = language['months'][date.month]
                day     = str(date.day)

                return day + " " + month + " " + year

            metadata_filepath = os.path.join(page_content_dirpath, 'index.yaml')

            if (os.path.exists(metadata_filepath)): 
        
                page = {
                    'path':             get_path(),                    
                    'dirname':          os.path.split(page_content_dirpath)[1],
                    'metadata':         read_yaml_file(metadata_filepath),
                    'attachments':      get_attachments(),
                    'content_dirpath':  page_content_dirpath,
                    'project_dirpath':  page_content_dirpath.replace(paths['content_pages_dirpath'], paths['project_dirpath'])
                }

                page['date'] = get_date()
                page['html'] = get_html()

            else:

                page = None

            return page

        texts = []
        notes = []

        folders = os.walk(paths['content_pages_dirpath'])

        for folder in folders:

            page_content_dirpath = folder[0]

            page = get_page()

            if (page != None):

                is_note = page_content_dirpath.startswith(paths['content_notes_dirpath'])

                if (is_note):
                    notes.append(page)
                else:
                    texts.append(page)
        
        notes = sorted(
            notes,
            key = lambda note: note['metadata']['created'],
            reverse = True
        )

        return {'texts': texts, 'notes': notes}

    def build_texts():

        def build_text():

            def get_template_parameters():

                result = get_standard_template_parameters(
                    text['metadata']['title'],
                    text['metadata']['description'],
                    text['path'],
                    text['path'],
                    True
                )

                result['text'] = text

                return result
                
            make_dir(text['project_dirpath'])

            template_parameters = get_template_parameters()
            rendered_template   = get_rendered_template('text.html', template_parameters)

            write_page(text['project_dirpath'], rendered_template)

        for text in pages['texts']:

            build_text()
            
            copy_page_attachments(text)

    def build_notes_pagination():

        def build_page(page_number):

            def get_template_parameters():

                def get_notes_page_url(page_number: int):

                    result = config['url'] + '/notes/'

                    if selected_tag != None:
                        result = result + 'tags/' + selected_tag + '/'

                    if page_number > 1:
                        result = result + 'page-' + str(page_number) + '/'

                    return result

                path = page_parent_path

                if page_dirname != '':
                    path = path + page_dirname + '/'

                result = get_standard_template_parameters(
                    language['notes'] if selected_tag == None else tags[selected_tag][:1].upper() + tags[selected_tag][1:],
                    language['notes_description'],
                    path,
                    path,
                    False
                )
                
                result['notes'] = page_notes
                result['tags']  = tags                
                
                result['selected_tag']      = selected_tag
                result['page_parent_path']  = page_parent_path

                if page_number == None:

                    result['page_later_url']    = ''
                    result['page_earlier_url']  = '' if is_last_page else get_notes_page_url(2)
                    
                else:

                    result['page_later_url']    = '' if page_number == 1 else get_notes_page_url(page_number - 1)
                    result['page_earlier_url']  = '' if is_last_page else get_notes_page_url(page_number + 1)

                result['hotkey_ctrl_up_url']    = result['page_later_url']
                result['hotkey_ctrl_down_url']  = result['page_earlier_url']

                return result

            if page_number == None:

                page_dirname = ''
                page_dirpath = page_parent_dirpath

            else:                

                page_dirname = 'page-' + str(page_number)
                page_dirpath = os.path.join(page_parent_dirpath, page_dirname)

            make_dir(page_dirpath)
            
            template_parameters = get_template_parameters()
            rendered_template   = get_rendered_template('notes.html', template_parameters)

            write_page(page_dirpath, rendered_template)

        if selected_tag == None:

            notes = pages['notes']

            page_parent_dirpath = paths['project_notes_dirpath']
            page_parent_path    = '/notes/'

        else:

            notes = get_notes_by_tag(pages['notes'], selected_tag)

            page_parent_dirpath = os.path.join(paths['project_notes_dirpath'], 'tags', selected_tag)
            page_parent_path    = '/notes/tags/' + selected_tag + '/'

        page_number = 1
        page_notes  = []
        page_size   = 20
        
        notes_left  = len(notes)
                
        for note in notes:
            
            page_notes.append(note)            
            notes_left -= 1

            if len(page_notes) == page_size or notes_left == 0:

                is_last_page = notes_left == 0

                if (page_number == 1):
                    build_page(None)

                build_page(page_number)

                page_number += 1
                page_notes   = []

    def build_notes():

        def build_note():

            def get_template_parameters():

                result = get_standard_template_parameters(
                    note['metadata']['title'],
                    note['metadata']['description'],
                    notes_parent_path + note['dirname'] + '/',
                    '/notes/{}/'.format(note['dirname']),
                    True
                )

                result['tags']          = tags
                result['selected_tag']  = selected_tag

                result['note'] = note

                result['note_after_url']        = '' if note_after == None else config['url'] + notes_parent_path + note_after['dirname'] + '/'
                result['note_after_title']      = '' if note_after == None else note_after['metadata']['title']

                result['note_earlier_url']      = '' if note_earlier == None else config['url'] + notes_parent_path + note_earlier['dirname'] + '/'
                result['note_earlier_title']    = '' if note_earlier == None else note_earlier['metadata']['title']
                
                result['hotkey_ctrl_right_url'] = result['note_after_url']
                result['hotkey_ctrl_left_url']  = result['note_earlier_url']

                return result
            
            template_parameters = get_template_parameters()
            rendered_template   = get_rendered_template('note.html', template_parameters)

            if selected_tag == None:
                note_filepath = note['project_dirpath']
            else:
                note_filepath = os.path.join(paths['project_notes_dirpath'], 'tags', selected_tag, note['dirname'])

            make_dir(note_filepath)

            write_page(note_filepath, rendered_template)

        if selected_tag == None:

            notes               = pages['notes']
            notes_parent_path   = '/notes/'

        else:

            notes               = get_notes_by_tag(pages['notes'], selected_tag)
            notes_parent_path   = '/notes/tags/' + selected_tag + '/'

        note_index      = 0
        note_index_max  = len(notes) - 1

        for note in notes:

            note_after      = None if note_index == 0 else notes[note_index - 1]
            note_earlier    = None if note_index == note_index_max else notes[note_index + 1]

            build_note()
                
            if selected_tag == None:
                copy_page_attachments(note)

            note_index += 1

    def build_tags_statistic():

        def get_template_parameters():

            def get_statistic():

                def get_tag_counters():

                    result = {}                

                    for note in pages['notes']:

                        for tag in note['metadata']['tags']:

                            if result.get(tag) == None:
                                result[tag] = 0

                            result[tag] += 1

                    return sorted(result.items(), key = lambda item: item[1], reverse = True)

                def get_plural_form(value, language_key):

                    plurals = language[language_key]
                        
                    form1 = plurals[1]
                    form2 = plurals[2]
                    form5 = plurals[5]
                    
                    if (value - value % 10) % 100 != 10:

                        if value % 10 == 1:
                            result = form1
                        elif value % 10 >= 2 and value % 10 <= 4:
                            result = form2
                        else: 
                            result = form5
                    
                    else:
                        result = form5
                    
                    return str(value) + ' ' + result

                result          = []
                tag_counters    = get_tag_counters()

                for tag_counter in tag_counters:

                    name    = tag_counter[0]
                    counter = get_plural_form(tag_counter[1], 'note_plural')

                    item = {'name': name, 'counter': counter}

                    result.append(item)

                return result

            result = get_standard_template_parameters(
                language['tags'],
                language['tags_description'],
                '/notes/tags/',
                '/notes/tags/',
                False
            )
                
            result['statistic'] = get_statistic()
            result['tags']      = tags                        

            return result

        dirpath = os.path.join(paths['project_notes_dirpath'], 'tags')

        make_dir(dirpath)

        template_parameters = get_template_parameters()
        rendered_template   = get_rendered_template('tags.html', template_parameters)

        write_page(dirpath, rendered_template)

    def build_sitemap():
        
        def get_template_parameters():
            
            def add_urls(urls, pages):

                def is_in_sitemap():

                    options = page['metadata'].get('options')
                
                    return True if options == None else 'no-sitemap' not in options

                for page in pages:

                    if is_in_sitemap():
                        
                        url = {
                            'loc':      config['url'] + page['path'],
                            'lastmod':  page['metadata']['changed'].strftime('%Y-%m-%d')
                        }

                        urls.append(url)

            urls = []

            add_urls(urls, pages['texts'])
            add_urls(urls, pages['notes'])

            return {'urls': urls}

        template_parameters = get_template_parameters()
        rendered_template   = get_rendered_template('sitemap.xml', template_parameters)

        filepath = os.path.join(paths['project_dirpath'], 'sitemap.xml')

        write_file(filepath, rendered_template)

    def build_rss():

        def get_template_parameters():

            def get_items():

                def is_in_rss():

                    options = note['metadata'].get('options')
                
                    return True if options == None else 'no-rss' not in options

                items = []

                for note in pages['notes']:
                    
                    if is_in_rss():

                        item = {
                            'title':        note['metadata']['title'],
                            'link':         config['url'] + note['path'],
                            'guid':         'note-' + note['dirname'],
                            'pub_date':     note['metadata']['created'].strftime('%a, %d %b %Y %H:%M:%S +0700'),
                            'description':  note['html']
                        }

                        items.append(item)

                        if len(items) == 10:
                            break

                return items

            return {
                'items': get_items()
            }

        template_parameters = get_template_parameters()
        rendered_template   = get_rendered_template('rss.xml', template_parameters)

        filepath = os.path.join(paths['project_dirpath'], 'rss.xml')

        write_file(filepath, rendered_template)

    def build_page_404():

        template_parameters = get_standard_template_parameters(language['page_404_title'], language['page_404_text'], '', '', False)
        rendered_template   = get_rendered_template('404.html', template_parameters)

        filepath = os.path.join(paths['project_dirpath'], '404.html')

        write_file(filepath, rendered_template)

    def build_robots():

        rendered_template = get_rendered_template('robots.txt')
        filepath = os.path.join(paths['project_dirpath'], 'robots.txt')

        write_file(filepath, rendered_template)

    def copy_assets():

        assets_dirpath = os.path.join(BUILDER_DIRPATH, 'assets')    
        result_dirpath = paths['project_dirpath']

        for item in os.listdir(assets_dirpath):

            source_path = os.path.join(assets_dirpath, item)
            result_path = os.path.join(result_dirpath, item)
            
            if os.path.isdir(source_path):
                shutil.copytree(source_path, result_path)
            else:
                shutil.copy2(source_path, result_path)

    def get_standard_template_parameters(page_title, page_description, page_path, page_base_path, editable = True):

        def get_page_edit_path(page_base_path, editable):

            if editable:

                if config['github_repository'] != '':
                    result = 'https://github.com/{}/edit/main/pages{}index.md'.format(config['github_repository'], page_base_path)
                else:
                    result = ''

            else:

                result = ''

            return result

        page_edit_path = get_page_edit_path(page_base_path, editable)

        #print(page_path + ": " + page_edit_path)
    
        return {
            'page_title':           page_title,
            'page_description':     page_description,
            'page_path':            page_path,
            'page_edit_path':       page_edit_path,
        }

    def get_rendered_template(filename: str, parameters: dict = {}):
        
        template = templates.get_template(filename)

        parameters['language']  = language
        parameters['config']    = config

        return template.render(parameters)

    def get_notes_by_tag(notes: list, tag: str):

        result = []

        for note in notes:

            if tag in note['metadata']['tags']:
                result.append(note)

        return result

    def copy_page_attachments(page: dict):
        
        for attachment in page['attachments']:

            content_filepath = os.path.join(page['content_dirpath'], attachment)
            project_filepath = os.path.join(page['project_dirpath'], attachment)

            shutil.copyfile(content_filepath, project_filepath)

    def write_page(dirpath: str, content: str):

        filepath = os.path.join(dirpath, 'index.html')

        with open(filepath, "w+", encoding = 'utf-8-sig') as file:
            file.write(content)

    def write_file(filepath: str, content: str):

        with open(filepath, "w+", encoding = 'utf-8-sig') as file:
            file.write(content)            

    def make_dir(path):

        if (not os.path.exists(path)):
            os.mkdir(path)

    templates   = get_templates()
    language    = get_language()
    tags        = get_tags()
    pages       = get_pages()

    build_texts()

    selected_tag = None

    build_notes_pagination()
    build_notes()
    
    build_tags_statistic()
    
    for selected_tag in tags:

        build_notes_pagination()
        build_notes()

    build_sitemap()
    build_rss()

    build_page_404()
    build_robots()

    copy_assets()

def read_yaml_file(yaml_filepath):

    with open(yaml_filepath, encoding = 'utf-8-sig') as yaml_file:
        result = yaml.safe_load(yaml_file)

    return result

BUILDER_DIRPATH = os.path.abspath(os.path.dirname(__file__))

args    = get_args()
config  = get_config()
paths   = get_paths()

clear_project()
build_project()