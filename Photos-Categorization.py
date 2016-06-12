# coding: utf-8
import exifread
import os
import shutil
import hashlib


class Photo:
    def __init__(self, fromPath, toPath):
        # source path where your photos are
        self.fromPath = fromPath
        # destination path where put your photos to
        self.toPath = toPath
        # counter
        self.totalPhotos = 1
        self.md5List = []
        self.samePhotos = 0
        self.picFormats = ['.jpg','.JPG','.jpeg','.JPEG','.png','.PNG']

    def getYMD(self, filename):
        """
        Get year, month, day, hour, minute, second of the image
        :param filename: file name of the image
        :return: year, month, day, hour, minute, second
        """
        file = open(filename)
        r,e = os.path.split(filename)
        if e in self.picFormats:
            md5 = hashlib.md5(open(filename).read()).hexdigest()
            if(md5 not in self.md5List):
                self.md5List.append(md5)
            else:
                print '!!Find the same files!!'
                self.samePhotos += 1
                return None,None,None,None,None,None
        # tags is a dictionary stores image's exif information
        tags = exifread.process_file(file)
        # if do not find exif information, set default date
        if len(tags) == 0:
            date = '1970:01:01'
            time = '00:00:00'
        else:
            # temp has the format "1970:01:01 00:00:00"
            if tags.has_key('EXIF DateTimeOriginal'):
                temp = str(tags['EXIF DateTimeOriginal'])
            elif tags.has_key('Image DateTime'):
                temp = str(tags['Image DateTime'])
            else:
                temp = '1970:01:01 00:00:00'
            date, time = str.split(temp, ' ')
        year, month, day = date.split(':')
        hour, minute, second = time.split(':')
        return year, month, day, hour, minute, second

    def renameAllFiles(self):
        """
        Rename all images and move to property location
        :return: none
        """
        if os.path.isdir(self.fromPath):
            # traversal all file in source path
            for root, dirs, files in os.walk(self.fromPath):
                for name in files:
                    print root, name
                    if (root[-1] != '/'):
                        filename = str(root) + '/' + str(name)
                    else:
                        filename = str(root) + str(name)
                    # get root and extension name
                    r, extension = os.path.splitext(filename)
                    # get date
                    year, month, day, hour, min, sec = self.getYMD(filename)
                    if year == None:
                        continue
                    # get new file name
                    newFileName = str(year) + '-' + str(month) + '-' + str(day) + '-' + str(hour) + ':' + str(
                        min) + '-' + str(self.totalPhotos) + extension
                    # judge whether the folder exists, if not, make directory
                    save2Path = self.toPath + '/' + year + '/' + year + '-' + month
                    if (not os.path.isdir(save2Path)):
                        os.makedirs(save2Path)
                    # counter plus 1
                    self.totalPhotos += 1
                    # move file to property place
                    shutil.move(filename, save2Path + '/' + newFileName)

    def removeEmptyFolders(self, path):
        """
        remove empty folders
        :param path: remove empty folder under path
        :return: none
        """
        for root, dirs, files in os.walk(path):
            for dir in dirs:
                if os.listdir(root + '/' + dir) == []:
                    os.rmdir(root + '/' + dir)

    def getMd5(self,filename):
        return hashlib.md5(open(filename,'rb').read()).hexdigest()

src = raw_input('Enter source path:').encode('utf-8')
dst = raw_input('Enter destination path:').encode('utf-8')
p = Photo(src, dst)
p.renameAllFiles()
p.removeEmptyFolders(p.fromPath)
print 'Total images: %d \nTotal same images: %d' % (p.totalPhotos, p.samePhotos)
