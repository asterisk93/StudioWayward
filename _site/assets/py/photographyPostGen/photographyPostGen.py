#A quick script for generating picture object markdown files

######variables######

#number of photos in set
picQuantity = 0

#photoset identifier
keyword = ''

#base date of set creation (YYYY-MM-DD)
baseDate = '0000-00-00'


for imgNum in range(1, picQuantity + 1):

    #create filename
    filename = baseDate + '-' + keyword + '-' + str(imgNum) + '.markdown'

    #create frontmatter
    front = '---\n' + 'layout: post\n' + 'type: photography, picture\n' + 'permalink: /photography/:title\n' + 'title: ' + keyword + '-' + str(imgNum) + '\n' + 'date: ' + baseDate + '\n' + 'keyword: ' + keyword + '\n' + 'path: ' + str(imgNum) + '.jpg\n' + '---'

    #write to file
    fp = open((filename), 'x')
    fp.write(str(front + '\n\n\n'))
    fp.close()
            
    #tracking
    print(keyword + '-' + str(imgNum) + ' created')
