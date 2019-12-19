import re
import os
import uuid
import mwclient
import optparse


parser = optparse.OptionParser()
parser.add_option('-u', '--username', help="the wiki username (required)")
parser.add_option('-p', '--password', help="the wiki password (required)")
parser.add_option('-d', '--dry-run', action="store_true", dest='dry', help="perform a dry run (create no changes)")
options, args = parser.parse_args()

if not options.dry and (not options.username or not options.password):
    parser.error("username and password are required, when not running in dry mode")


ua = 'guid-fixer (User:N0emis)'
site = mwclient.Site('events.ccc.de', path='/congress/2019/wiki/', clients_useragent=ua)
#site = mwclient.Site('noemis.me', clients_useragent=ua)

if not options.dry:
    site.login(options.username, options.password)
else:
    print('Performing dry run')

category = site.categories['Session']

guids = []

for page in category:
    #print(page.name)
    #print('touched',page.touched)

    if page.can('edit') or options.dry:
        text = page.text()
        changed = False
        page_guids = re.findall("(\|GUID=)([\w-]*)$", text, re.M)

        for guid in page_guids:
            if guid[1] in guids:
                changed = True
                new_guid = uuid.uuid4()
                text = text.replace(guid[1], str(new_guid), 1)
                guids.append(new_guid)
                print("replacing GUID {} with {} on {}".format(guid[1], new_guid, page.name))
            else:
                guids.append(guid[1])
        if changed and not options.dry:
            page.save(text, 'uniquifying session GUID', minor=True, bot=True)
    else:
        print("You are not allowed to edit the page {}. Please check your permissions...".format(page.name))
