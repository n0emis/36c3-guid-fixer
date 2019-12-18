import re
import os
import uuid
import mwclient


ua = 'guid-fixer (User:N0emis)'
site = mwclient.Site('events.ccc.de', path='/congress/2019/wiki/', clients_useragent=ua)

site.login(os.environ['WIKI_USERNAME'] ,os.environ['WIKI_PASSWORD'])

category = site.categories['Session']

guids = []

for page in category:
    #print(page.name)
    #print('touched',page.touched)

    if page.can('edit'):
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
        if changed:
            page.save(text, 'uniquifying session GUID', minor=True, bot=True)
    else:
        print("You are not allowed to edit the page {}. Please check your permissions...".format(page.name))
