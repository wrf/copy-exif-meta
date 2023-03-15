# copy-exif-meta
Code to automate copying of EXIF metadata from video to framegrabs, specifically to have the video metadata transferred to VLC framegrabs. These are all wildlife shots where I then use the images for [iNaturalist](https://www.inaturalist.org/), which can read the metadata or species names from the filename.

### short version ###
Framegrabs are taken from videos using [VLC](https://www.videolan.org/vlc/), by the `Take Snapshot` command in the `Video` menu.

The script takes all framegrabs as `.jpg` that have a match of the first 8 letters of any of the videos as `.MP4`. The 8 characters comes from the length of numbered filenames from the goPro camera, e.g. `GX010962`. For each image with a matching video, a line of a shell script is generated, and written to `stdout`.

`copy_exif_data_to_framegrabs.py -f framegrabs/*.jpg -m working_set/*.MP4 > exif_script.sh`

`sh exif_script.sh`

### long version ###

![photo framegrab of blue ring angelfish](https://github.com/wrf/copy-exif-meta/blob/main/images/GX010962_bluering_angelfish_good.MP4__00_00_01--2023-03-15-09h56m22s014.jpg)

The goPro videos have many metadata fields, which are not copied to the snapshots.

```
$ exiftool working_set/GX010962_bluering_angelfish_good.MP4 
ExifTool Version Number         : 11.88
File Name                       : GX010962_bluering_angelfish_good.MP4
Directory                       : working_set
File Size                       : 97 MB
File Modification Date/Time     : 2023:03:02 21:16:09+07:00
File Access Date/Time           : 2023:03:15 09:56:46+07:00
File Inode Change Date/Time     : 2023:03:15 09:56:28+07:00
File Permissions                : rwxr-xr-x
File Type                       : MP4
File Type Extension             : mp4
MIME Type                       : video/mp4
Major Brand                     : MP4 v1 [ISO 14496-1:ch13]
Minor Version                   : 2013.10.18
Compatible Brands               : mp41
Media Data Size                 : 101160310
Media Data Offset               : 28
Movie Header Version            : 0
Create Date                     : 2023:03:02 14:16:00
Modify Date                     : 2023:03:02 14:16:00
Time Scale                      : 60000
Duration                        : 8.07 s
Preferred Rate                  : 1
Preferred Volume                : 100.00%
Preview Time                    : 0 s
Preview Duration                : 0 s
Poster Time                     : 0 s
Selection Time                  : 0 s
Selection Duration              : 0 s
Current Time                    : 0 s
Next Track ID                   : 6
Lens Serial Number              : LKO1030802400767
Camera Serial Number Hash       : 7ad2e98542eca01cbd9aad49fb3ef4ad
Firmware Version                : HD9.01.01.72.00
Camera Serial Number            : C3441326346455
Camera Model Name               : HERO9 Black
Auto Rotation                   : Up
Digital Zoom                    : No
Pro Tune                        : On
White Balance                   : AUTO
Sharpness                       : MED
Color Mode                      : GOPRO
Auto ISO Max                    : 1600
Auto ISO Min                    : 100
Exposure Compensation           : -0.5
Rate                            : 2_1SEC
Field Of View                   : Linear
Electronic Image Stabilization  : HS Boost
Audio Setting                   : STEREO
Device Name                     : Highlights
Track Header Version            : 0
Track Create Date               : 2023:03:02 14:16:00
Track Modify Date               : 2023:03:02 14:16:00
Track ID                        : 1
Track Duration                  : 8.07 s
Track Layer                     : 0
Track Volume                    : 0.00%
Image Width                     : 3840
Image Height                    : 2160
Graphics Mode                   : srcCopy
Op Color                        : 0 0 0
Compressor ID                   : hvc1
Source Image Width              : 3840
Source Image Height             : 2160
X Resolution                    : 72
Y Resolution                    : 72
Compressor Name                 : GoPro H.265 encoder
Bit Depth                       : 24
Video Frame Rate                : 59.94
Time Code                       : 3
Balance                         : 0
Audio Format                    : mp4a
Audio Channels                  : 2
Audio Bits Per Sample           : 24
Audio Sample Rate               : 48000
Text Font                       : Unknown (21)
Text Face                       : Plain
Text Size                       : 10
Text Color                      : 0 0 0
Background Color                : 65535 65535 65535
Font Name                       : Helvetica
Other Format                    : tmcd
Warning                         : [minor] The ExtractEmbedded option may find more tags in the media data
Matrix Structure                : 1 0 0 0 1 0 0 0 1
Media Header Version            : 0
Media Create Date               : 2023:03:02 14:16:00
Media Modify Date               : 2023:03:02 14:16:00
Media Time Scale                : 60000
Media Duration                  : 8.07 s
Handler Class                   : Media Handler
Handler Type                    : NRT Metadata
Handler Description             : GoPro SOS
Gen Media Version               : 0
Gen Flags                       : 0 0 0
Gen Graphics Mode               : srcCopy
Gen Op Color                    : 0 0 0
Gen Balance                     : 0
Meta Format                     : fdsc
Image Size                      : 3840x2160
Megapixels                      : 8.3
Avg Bitrate                     : 100 Mbps
Rotation                        : 0
```

When taking a framegrab with [VLC](https://www.videolan.org/vlc/), most of this metadata is lost, shown below:

```
$ exiftool framegrabs/GX010962_bluering_angelfish_good.MP4__00_00_01--2023-03-15-09h56m22s014.jpg 
ExifTool Version Number         : 11.88
File Name                       : GX010962_bluering_angelfish_good.MP4__00_00_01--2023-03-15-09h56m22s014.jpg
Directory                       : framegrabs
File Size                       : 2.2 MB
File Modification Date/Time     : 2023:03:15 09:56:22+07:00
File Access Date/Time           : 2023:03:15 09:56:22+07:00
File Inode Change Date/Time     : 2023:03:15 09:56:22+07:00
File Permissions                : rw-rw-r--
File Type                       : JPEG
File Type Extension             : jpg
MIME Type                       : image/jpeg
JFIF Version                    : 1.01
Resolution Unit                 : None
X Resolution                    : 1
Y Resolution                    : 1
Image Width                     : 3840
Image Height                    : 2160
Encoding Process                : Baseline DCT, Huffman coding
Bits Per Sample                 : 8
Color Components                : 3
Y Cb Cr Sub Sampling            : YCbCr4:2:0 (2 2)
Image Size                      : 3840x2160
Megapixels                      : 8.3
```

Running the script `copy_exif_data_to_framegrabs.py` collects all images `-f` that have a matching basename with any videos `-m`, and writes the `exiftool` commands to a shell script. The commands would appear as below, with the straightforward option `-TagsFromFile` to copy metadata tags:

`exiftool -TagsFromFile working_set/GX010962_bluering_angelfish_good.MP4 framegrabs/GX010962_bluering_angelfish_good.MP4__00_00_01--2023-03-15-09h56m22s014.jpg`

This is run as a shell script. It typically produces a warning about some of the metadata fields that cannot be copied for JPEGs.

```
$ exiftool -TagsFromFile working_set/GX010962_bluering_angelfish_good.MP4 framegrabs/GX010962_bluering_angelfish_good.MP4__00_00_01--2023-03-15-09h56m22s014.jpg
Warning: [minor] The ExtractEmbedded option may find more tags in the media data - working_set/GX010962_bluering_angelfish_good.MP4
    1 image files updated
```

Fields including camera model and timestamp are then copied:

```
$ exiftool framegrabs/GX010962_bluering_angelfish_good.MP4__00_00_01--2023-03-15-09h56m22s014.jpg
ExifTool Version Number         : 11.88
File Name                       : GX010962_bluering_angelfish_good.MP4__00_00_01--2023-03-15-09h56m22s014.jpg
Directory                       : framegrabs
File Size                       : 2.2 MB
File Modification Date/Time     : 2023:03:15 10:00:42+07:00
File Access Date/Time           : 2023:03:15 10:00:42+07:00
File Inode Change Date/Time     : 2023:03:15 10:00:42+07:00
File Permissions                : rw-rw-r--
File Type                       : JPEG
File Type Extension             : jpg
MIME Type                       : image/jpeg
JFIF Version                    : 1.01
Exif Byte Order                 : Big-endian (Motorola, MM)
Camera Model Name               : HERO9 Black
X Resolution                    : 72
Y Resolution                    : 72
Resolution Unit                 : None
Modify Date                     : 2023:03:02 14:16:00
Y Cb Cr Positioning             : Centered
Exif Version                    : 0232
Create Date                     : 2023:03:02 14:16:00
Components Configuration        : Y, Cb, Cr, -
Exposure Compensation           : -1/2
Flashpix Version                : 0100
Color Space                     : Uncalibrated
White Balance                   : Auto
Lens Serial Number              : LKO1030802400767
Camera Serial Number            : C3441326346455
XMP Toolkit                     : Image::ExifTool 11.88
Audio Bits Per Sample           : 24
Minor Version                   : 2013.10.18
Audio Sample Rate               : 48000
Video Frame Rate                : 59.94
Font Name                       : Helvetica
Image Width                     : 3840
Image Height                    : 2160
Encoding Process                : Baseline DCT, Huffman coding
Bits Per Sample                 : 8
Color Components                : 3
Y Cb Cr Sub Sampling            : YCbCr4:2:0 (2 2)
Image Size                      : 3840x2160
Megapixels                      : 8.3
```




