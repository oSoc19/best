# Require any additional compass plugins here.
# require "susy"
#require "sass-globbing"
# require "breakpoint"

#Folder settings
project_type = :stand_alone
http_path = "/"
relative_assets = true      #because we're not working from the root
css_dir = "css"          #where the CSS will saved
sass_dir = "css"           #where our .scss files are
images_dir = "img"    #the folder with your images
javascripts_dir = "js"

# You can select your preferred output style here (can be overridden via the command line):
output_style = :expanded # After dev :compressed

# To disable debugging comments that display the original location of your selectors. Uncomment:
line_comments = false

# Obviously
preferred_syntax = :scss

# Sourcemaps for Chrome DevTools

sass_options = {:sourcemap => true}
# sass_options = {:debug_info => true}
sourcemap = true