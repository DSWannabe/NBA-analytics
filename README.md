# NBA-analytics
A basketball lover

# Note on web scraping
in a table you have:
- tr : table row
- td : table data

KeywordsP
- drop list
- button
- radio button

# Clean data
- Seasonal stats of each player cannot be null
    - if null, go find that stat or replace it with something else: In reality all player of a season has to have stats either they play or not
    - outliers: each stats only go within a specific range

# Note on git
- Normal git commit can't work with files larger than 100MB, so use git LFS
- Some files are not meant to be commited (cache). So run "git rm <file_path>
- Create a backup directory to make sure we have a backup version
- .pyc files are usually redundant (python cache), can ignore them
- # Some common cmds to work with git:
-- git status: Check merge status 
-- 
