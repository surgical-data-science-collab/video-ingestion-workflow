import os
import pandas as pd
import numpy as np
from lxml import etree
import re


"""
convert_frame_object_to_xml. This is the PASCAL VOC format
Given a frame object and a file path, convert it to an xml and save at the path
"""
def convert_frame_object_to_xml(frame_obj, destination, prefix=''):
    # create the file structure and add in xml attributes
    annotation = etree.Element('annotation')
    annotation.set('verified', 'yes')

    #name contains the entire file path and filename, so remove any path part (everything before the last / )
    frame_file_name = os.path.split(frame_obj["name"])[1]
    
    folder = etree.SubElement(annotation, 'folder')
    folder.text = 'images'
    
    filename = etree.SubElement(annotation, 'filename')
    filename.text = frame_file_name

    path = etree.SubElement(annotation, 'path')
    path.text = os.path.join(destination, frame_file_name)
    
    source = etree.SubElement(annotation, 'source')
    
    database = etree.SubElement(source, 'database')
    database.text = frame_obj["database"]
    
    size = etree.SubElement(annotation, 'size')
    for i in [['width', frame_obj['width']], ['height', frame_obj['height']], ['depth', 3]]:
        ele = etree.SubElement(size, i[0])
        ele.text = str(int(i[1]))
        
    segmented = etree.SubElement(annotation, 'segmented')
    segmented.text = '0'

    #for each tool, add the tool name and the bounding box coordinates
    for t in frame_obj['tools']:            
        obj = etree.SubElement(annotation, 'object')
        
        for i in [['name', t['type']], ['pose', 'Unspecified'], ['truncated', 0], ['difficult', 0]]:
            n = etree.SubElement(obj, i[0])
            n.text = str(i[1])
        
        bndbox = etree.SubElement(obj, 'bndbox')
        for i in [
            ['xmin', t['coordinates'][0][0]], ['ymin', t['coordinates'][0][1]], 
            ['xmax', t['coordinates'][1][0]], ['ymax', t['coordinates'][1][1]]
        ]:
            bele = etree.SubElement(bndbox, i[0])
            bele.text = str(int(i[1]))
        
    # create a new XML file with the results using the same
    # replace the .jpeg extension with .xml (keep same file name) and create a file to write data to
    # print(os.path.join(destination, re.sub(r".jpeg|.jpg", '.xml', frame_file_name)))

    xml_file_name = re.sub(r".jpeg|.jpg", '.xml', frame_file_name)

    if("xml" in xml_file_name):
        myfile = open(os.path.join(destination, xml_file_name), "wb")
        myfile.write(etree.tostring(annotation, pretty_print=True))
        myfile.close()

def main():

    '''
        Check to make sure that the input .csv file of detections/ground truths contains the following columns:
            "trial_frame" : filename for each frame (includes the trial and the frame number)
            "label" : annotation label for the tool
            "x1" : first x coordinate (xmin)
            "x2" : second x coordinate (xman)
            "y1" : first y coordinate (ymin)
            "y2" : second y coordinate (ymax)

            Either the columns must be named as above, OR must be in the order above
    '''

    #read in the ground-truth annotations with the approtriate column names (based on the csv file)
    ground_truth = pd.read_csv("D:\\so-spine\\spine_bounding_boxes_edited.csv", names=["trial_frame", "label", "x1", "x2", "y1", "y2"], header=0)
    # ground_truth = pd.read_csv("socal.csv", names=["trial_frame", "x1", "y1", "x2", "y2", "label"])

    #directory that contains all the dataset information...including images and annotation output folder
    BASE_FILE_PATH =  "D:\\so-spine"
    #BASE_FILE_PATH = "C:\\Users\\reach\\Documents\\SOCAL\\frames"

    #database name
    database = "SoSpine-Ground-Truth"

    #path to save xmls to
    FRAME_XML_PATH = os.path.join(BASE_FILE_PATH, "Pascal Format XML Annotations Edited")

    #path that contains the JPEG images
    FRAME_JPG_PATH = os.path.join(BASE_FILE_PATH, "images")

    #basically create a xml for each frame (NOT for each tool identified)
    for unique_frames in ground_truth.groupby(["trial_frame"]):

        is_nan = False
        file_path = os.path.join(FRAME_JPG_PATH, unique_frames[0])

        #assumes all images have the same dimensions
        img_width = 1920
        img_height = 1080

        tools = []

        for index, row in unique_frames[1].iterrows():  #for each tool in that frame

            is_nan = False   #to keep track of frame having no tools

            if(pd.isna(row["label"])):

                is_nan = True  #exit for loop it frame has no tools (no tools/bounding boxes needed)
                break

            tools.append({ 
            'type': row["label"], 
            'coordinates': [
                (row["x1"], row["y1"]),
                (row["x2"], row["y2"])
            ]})

        #create the frame object dict to feed into the xml creator function
        if(is_nan == False):

            frame_data = {
            'database': database,
            'name': file_path,
            'width': img_width,
            'height': img_height,
            'tools': tools 
            }

        else:   #if there are no tools, create an XML without any annotations. Just the image info
            frame_data = {
            'database': database,
            'name': file_path,
            'width': img_width,
            'height': img_height,
            'tools': [] 
            }

        #convert the frame object to an xml file and save it to the correct path
        convert_frame_object_to_xml(frame_data, FRAME_XML_PATH)

if __name__ == "__main__":
    main()