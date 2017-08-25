import requests
from bs4 import BeautifulSoup
import re

# Load any old page on the website
result = requests.get("https://www.smith.edu/libraries/givemea404")
c = result.content
soup = BeautifulSoup(c, "html5lib")

## SUBTRACT ##
# Delete Drupal generator meta tag and Google site verification meta tag
metatagsToDelete = ['generator', 'google-site-verification']
for element in soup.find_all("meta", {'name': metatagsToDelete}):
    element.decompose()

# Delete Drupal generated css includes to agrigated css files
for element in soup.find_all("link", {'href':re.compile("https://www.smith.edu/libraries/sites/libraries/files/css/css_(.*?)\.css")}):
    element.decompose()

# Delete main content
soup.select("#skipToContent > section")[0].decompose()

# Delete ALL javascript (including Drupal agrigated js files)
#for element in soup.find_all('script'):
#    element.decompose()
import pdb; pdb.set_trace()
# Delete Drupal generated js includes to agrigated js files
for element in soup.find_all("script", {'src':re.compile("https://www.smith.edu/libraries/sites/libraries/files/js/js_(.*?)\.js")}):
    element.decompose()

## ADD ##
# Add Drupal system base and main style link to site css
head = soup.find("head")
cssSources = ["https://www.smith.edu/libraries/modules/system/system.base.css", "https://www.smith.edu/libraries/sites/libraries/themes/smith_library/css/main-styles.css"]
for cssSource in cssSources:
    newTag = soup.new_tag("link", href=cssSource, rel="stylesheet", type="text/css")
    head.append(newTag)

## Add various js includes
jsSources = ['https://www.smith.edu/libraries/sites/libraries/themes/smith_library/ui/scripts/vendor/jquery/jquery-1.9.1.min.js', 'https://use.fontawesome.com/e8941a2fd6.js', 'https://www.smith.edu/libraries/sites/libraries/themes/smith_library/ui/scripts/vendor/modernizr/modernizr.custom.js']
for jsSource in jsSources:
    newTag = soup.new_tag('script', src=jsSource)
    head.append(newTag)

# Add require.js to bottom with data-main attribute
body = soup.find("body")
newTag = soup.new_tag('script', src="https://www.smith.edu/libraries/sites/libraries/themes/smith_library/ui/scripts/vendor/require/require.js")
newTag['data-main'] = "https://www.smith.edu/libraries/sites/libraries/themes/smith_library/ui/scripts/main"
body.append(newTag)
#body.append('<script data-main="https://www.smith.edu/libraries/sites/libraries/themes/smith_library/ui/scripts/main" src="https://www.smith.edu/libraries/sites/libraries/themes/smith_library/ui/scripts/vendor/require/require.js"></script>')

demoContent = """
  <div class="container">
    <div class="row">
      <h1>Content Goes Here</h1>
      <p>
        Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.
      </p>
      <p>
        Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.
      </p>
      <p>
        Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.
      </p>
    </div>
  </div>
"""
demoContentSoup = BeautifulSoup(demoContent, 'html5lib')
soup.select("#skipToContent")[0].append(demoContentSoup.find("div"))

# Write full page template
output = soup.prettify(formatter="html")
with open("smith-libraries-template-full.html", "w") as f:
    f.write(output)

# Now make one without the hours and subnav

# Now make one without the hours and the whole nav
