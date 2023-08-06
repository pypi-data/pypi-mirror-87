import cv2
import numpy as np
from random import randint
import math
import os
from PIL import Image
import matplotlib.pyplot as plt

currentDirPath = os.getcwd()

protoFile = currentDirPath+"/pose/coco/pose_deploy_linevec.prototxt"
weightsFile = currentDirPath+"/pose/coco/pose_iter_440000.caffemodel"
nPoints = 18

# COCO Output Format

keypointsMapping = ['Nose', 'Neck', 'R-Sho', 'R-Elb', 'R-Wr', 'L-Sho',
                    'L-Elb', 'L-Wr', 'R-Hip', 'R-Knee', 'R-Ank', 'L-Hip',
                    'L-Knee', 'L-Ank', 'R-Eye', 'L-Eye', 'R-Ear', 'L-Ear']

POSE_PAIRS = [[1,2], [1,5], [2,3], [3,4], [5,6], [6,7],
              [1,8], [8,9], [9,10], [1,11], [11,12], [12,13],
              [1,0], [0,14], [14,16], [0,15], [15,17],
              [2,17], [5,16]]

# index of pafs correspoding to the POSE_PAIRS
# e.g for POSE_PAIR(1,2), the PAFs are located at indices (31,32) of output, Similarly, (1,5) -> (39,40) and so on.
mapIdx = [[31,32], [39,40], [33,34], [35,36], [41,42], [43,44],
          [19,20], [21,22], [23,24], [25,26], [27,28], [29,30],
          [47,48], [49,50], [53,54], [51,52], [55,56],
          [37,38], [45,46]]

colors = [ [0,100,255], [0,100,255], [0,255,255], [0,100,255], [0,255,255], [0,100,255],
         [0,255,0], [255,200,100], [255,0,255], [0,255,0], [255,200,100], [255,0,255],
         [0,0,255], [255,0,0], [200,200,0], [255,0,0], [200,200,0], [0,0,0]]


InitialimagePath = "frames/frame1.jpg"
FinalimagePath = "frames/frame45.jpg"


os.makedirs('./images/',exist_ok=True)



class ROM():


        def videotoimageconverter(path):
            vidObj = cv2.VideoCapture(path)


            # Used as counter variable
            count = 0
            # checks whether frames were extracted
            success = 1


            if not os.path.exists(currentDirPath+'/frames'):
                os.makedirs(currentDirPath+'/frames')

            while success:

                # vidObj object calls read
                # function extract frames
                success, image = vidObj.read()
                try:
                    # block raising an exception
                    cv2.imwrite(currentDirPath+"/frames/frame%d.jpg" % count, image)
                except:
                    pass # doing nothing on exception

                # Saves the frames with frame-count

                count += 1

            '''for i in range(0,count-1):
                img  = Image.open(currentDirPath+"frames/frame%d.jpg" % i)
                imgplot = plt.imshow(img)
                plt.show()'''


        def readFrame(a,b):

                image1 = cv2.imread(a)
                image2 = cv2.imread(b)
                InitialframeWidth = image1.shape[1]
                InitialframeHeight = image1.shape[0]
                FinalframeWidth = image2.shape[1]
                FinalframeHeight = image2.shape[0]

                Initialnet = cv2.dnn.readNetFromCaffe(protoFile, weightsFile)
                finalnet = cv2.dnn.readNetFromCaffe(protoFile, weightsFile)
                # Fix the input Height and get the width according to the Aspect Ratio
                inHeight = 368
                InitialinWidth = int((inHeight/InitialframeHeight)*InitialframeWidth)
                FinalinWidth = int((inHeight/FinalframeHeight)*FinalframeWidth)

                InitialinpBlob = cv2.dnn.blobFromImage(image1, 1.0 / 255, (InitialinWidth, inHeight),
                                          (0, 0, 0), swapRB=False, crop=False)
                FinalinpBlob = cv2.dnn.blobFromImage(image2, 1.0 / 255, (FinalinWidth, inHeight),
                                          (0, 0, 0), swapRB=False, crop=False)

                Initialnet.setInput(InitialinpBlob)
                finalnet.setInput(FinalinpBlob)
                Intialoutput = Initialnet.forward()
                Finaloutput = finalnet.forward()
                return Intialoutput,Finaloutput,InitialframeWidth,InitialframeHeight,FinalframeWidth,FinalframeHeight,image1,image2



        def getKeypoints(probMap, threshold=0.1):

            mapSmooth = cv2.GaussianBlur(probMap,(3,3),0,0)

            mapMask = np.uint8(mapSmooth>threshold)
            keypoints = []

            #find the blobs
            contours, _ = cv2.findContours(mapMask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

            #for each blob find the maxima
            for cnt in contours:
                blobMask = np.zeros(mapMask.shape)
                blobMask = cv2.fillConvexPoly(blobMask, cnt, 1)
                maskedProbMap = mapSmooth * blobMask
                _, maxVal, _, maxLoc = cv2.minMaxLoc(maskedProbMap)
                keypoints.append(maxLoc + (probMap[maxLoc[1], maxLoc[0]],))

            return keypoints


        def FetchingAnkleKeypoints(nPoints,output,imagePath):

            detected_keypoints = []
            keypoints_list = np.zeros((0,3))
            keypoint_id = 0
            threshold = 0.1
            image1 = cv2.imread(imagePath)
            for part in range(nPoints):
                probMap = output[0,part,:,:]
                probMap = cv2.resize(probMap, (image1.shape[1], image1.shape[0]))
            #     plt.figure()
            #     plt.imshow(255*np.uint8(probMap>threshold))
                keypoints = DeepFit.getKeypoints(probMap, threshold)
                if keypointsMapping[part] == 'R-Ank' :
                    return keypoints[0][:2]
                    break

                keypoints_with_id = []
                for i in range(len(keypoints)):
                    keypoints_with_id.append(keypoints[i] + (keypoint_id,))
                    keypoints_list = np.vstack([keypoints_list, keypoints[i]])
                    keypoint_id += 1

                detected_keypoints.append(keypoints_with_id)

            return keypoints





        def FetchingKneeKeypoint(nPoints,output,imagePath):

                detected_keypoints = []
                keypoints_list = np.zeros((0,3))
                keypoint_id = 0
                threshold = 0.1
                image1 = cv2.imread(imagePath)
                for part in range(nPoints):
                    probMap = output[0,part,:,:]
                    probMap = cv2.resize(probMap, (image1.shape[1], image1.shape[0]))
                #     plt.figure()
                #     plt.imshow(255*np.uint8(probMap>threshold))
                    keypoints = DeepFit.getKeypoints(probMap, threshold)
                    if keypointsMapping[part] == 'R-Knee' :
                        return keypoints[1][:2]
                        break

                    keypoints_with_id = []
                    for i in range(len(keypoints)):
                        keypoints_with_id.append(keypoints[i] + (keypoint_id,))
                        keypoints_list = np.vstack([keypoints_list, keypoints[i]])
                        keypoint_id += 1

                    detected_keypoints.append(keypoints_with_id)

                return keypoints


        def GetImageKeypoints(nPoints,output,imagePath):

            detected_keypoints = []
            keypoints_list = np.zeros((0,3))
            keypoint_id = 0
            threshold = 0.1
            image = cv2.imread(imagePath)

            for part in range(nPoints):
                probMap = output[0,part,:,:]
                probMap = cv2.resize(probMap, (image.shape[1], image.shape[0]))
           #     plt.figure()
           #     plt.imshow(255*np.uint8(probMap>threshold))
                keypoints = DeepFit.getKeypoints(probMap, threshold)
                if keypointsMapping[part] == 'R-Knee' and keypointsMapping[part] == 'R-Ank' and keypointsMapping[part] == 'L-Ank' and keypointsMapping[part] == 'L-Knee':
                    return keypoints[1][:2]
                    break

                keypoints_with_id = []
                for i in range(len(keypoints)):
                    keypoints_with_id.append(keypoints[i] + (keypoint_id,))
                    keypoints_list = np.vstack([keypoints_list, keypoints[i]])
                    keypoint_id += 1

                detected_keypoints.append(keypoints_with_id)


            return detected_keypoints,keypoints_list


        def getValidPairs(output,frameWidth,frameHeight,detected_keypoints):


                valid_pairs = []
                invalid_pairs = []
                n_interp_samples = 10
                paf_score_th = 0.1
                conf_th = 0.7
                # loop for every POSE_PAIR
                for k in range(len(mapIdx)):
                    # A->B constitute a limb
                    pafA = output[0, mapIdx[k][0], :, :]
                    pafB = output[0, mapIdx[k][1], :, :]
                    pafA = cv2.resize(pafA, (frameWidth, frameHeight))
                    pafB = cv2.resize(pafB, (frameWidth, frameHeight))

                    # Find the keypoints for the first and second limb
                    candA = detected_keypoints[POSE_PAIRS[k][0]]
                    candB = detected_keypoints[POSE_PAIRS[k][1]]
                    nA = len(candA)
                    nB = len(candB)

                    # If keypoints for the joint-pair is detected
                    # check every joint in candA with every joint in candB
                    # Calculate the distance vector between the two joints
                    # Find the PAF values at a set of interpolated points between the joints
                    # Use the above formula to compute a score to mark the connection valid

                    if( nA != 0 and nB != 0):
                        valid_pair = np.zeros((0,3))
                        for i in range(nA):
                            max_j=-1
                            maxScore = -1
                            found = 0
                            for j in range(nB):
                                # Find d_ij
                                d_ij = np.subtract(candB[j][:2], candA[i][:2])
                                norm = np.linalg.norm(d_ij)
                                if norm:
                                    d_ij = d_ij / norm
                                else:
                                    continue
                                # Find p(u)
                                interp_coord = list(zip(np.linspace(candA[i][0], candB[j][0], num=n_interp_samples),
                                                        np.linspace(candA[i][1], candB[j][1], num=n_interp_samples)))
                                # Find L(p(u))
                                paf_interp = []
                                for k in range(len(interp_coord)):
                                    paf_interp.append([pafA[int(round(interp_coord[k][1])), int(round(interp_coord[k][0]))],
                                                       pafB[int(round(interp_coord[k][1])), int(round(interp_coord[k][0]))] ])
                                # Find E
                                paf_scores = np.dot(paf_interp, d_ij)
                                avg_paf_score = sum(paf_scores)/len(paf_scores)

                                # Check if the connection is valid
                                # If the fraction of interpolated vectors aligned with PAF is higher then threshold -> Valid Pair
                                if ( len(np.where(paf_scores > paf_score_th)[0]) / n_interp_samples ) > conf_th :
                                    if avg_paf_score > maxScore:
                                        max_j = j
                                        maxScore = avg_paf_score
                                        found = 1
                            # Append the connection to the list
                            if found:
                                valid_pair = np.append(valid_pair, [[candA[i][3], candB[max_j][3], maxScore]], axis=0)

                        # Append the detected connections to the global list
                        valid_pairs.append(valid_pair)
                    else: # If no keypoints are detected
                        invalid_pairs.append(k)
                        valid_pairs.append([])
                return valid_pairs, invalid_pairs




        # For each detected valid pair, it assigns the joint(s) to a person
        # It finds the person and index at which the joint should be added. This can be done since we have an id for each joint
        def getPersonwiseKeypoints(valid_pairs,invalid_pairs,keypoints_list):
                # the last number in each row is the overall score
                personwiseKeypoints = -1 * np.ones((0, 19))

                for k in range(len(mapIdx)):
                    if k not in invalid_pairs:
                        partAs = valid_pairs[k][:,0]
                        partBs = valid_pairs[k][:,1]
                        indexA, indexB = np.array(POSE_PAIRS[k])

                        for i in range(len(valid_pairs[k])):
                            found = 0
                            person_idx = -1
                            for j in range(len(personwiseKeypoints)):
                                if personwiseKeypoints[j][indexA] == partAs[i]:
                                    person_idx = j
                                    found = 1
                                    break

                            if found:
                                personwiseKeypoints[person_idx][indexB] = partBs[i]
                                personwiseKeypoints[person_idx][-1] += keypoints_list[partBs[i].astype(int), 2] + valid_pairs[k][i][2]

                            # if find no partA in the subset, create a new subset
                            elif not found and k < 17:
                                row = -1 * np.ones(19)
                                row[indexA] = partAs[i]
                                row[indexB] = partBs[i]
                                # add the keypoint_scores for the two keypoints and the paf_score
                                row[-1] = sum(keypoints_list[valid_pairs[k][i,:2].astype(int), 2]) + valid_pairs[k][i][2]

                                personwiseKeypoints = np.vstack([personwiseKeypoints, row])
                return personwiseKeypoints




        def getKeypoints(probMap, threshold=0.1):


            mapSmooth = cv2.GaussianBlur(probMap,(3,3),0,0)

            mapMask = np.uint8(mapSmooth>threshold)
            keypoints = []

            #find the blobs
            contours, _ = cv2.findContours(mapMask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

            #for each blob find the maxima
            for cnt in contours:
                blobMask = np.zeros(mapMask.shape)
                blobMask = cv2.fillConvexPoly(blobMask, cnt, 1)
                maskedProbMap = mapSmooth * blobMask
                _, maxVal, _, maxLoc = cv2.minMaxLoc(maskedProbMap)
                keypoints.append(maxLoc + (probMap[maxLoc[1], maxLoc[0]],))

            return keypoints


                   
            


        def getROM(path):
            ROM.videotoimageconverter(path)
            print("Video got uploaded \nVideo to Frames coversion is done\nCalculating ROM ...")
            InitialOutput,FinalOutput,frameWidth1,frameHeight1,frameWidth2,frameHeight2,image1,image2 = ROM.readFrame(InitialimagePath,FinalimagePath)
            KneePoint = ROM.FetchingKneeKeypoint(18,InitialOutput,InitialimagePath)
            InitialAnklePoints = ROM.FetchingAnkleKeypoints(18,InitialOutput,InitialimagePath)
            FinalAnklePoints = ROM.FetchingAnkleKeypoints(18,FinalOutput,FinalimagePath)
            GetFirstImagePoints,FirstKeylist = ROM.GetImageKeypoints(18,InitialOutput,InitialimagePath)
            GetSecondImagePoints,SecondKeylist = ROM.GetImageKeypoints(18,FinalOutput,FinalimagePath)
            I_valid_pairs, I_invalid_pairs = ROM.getValidPairs(InitialOutput,frameWidth1,frameHeight1,GetFirstImagePoints)

            F_valid_pairs, F_invalid_pairs = ROM.getValidPairs(FinalOutput,frameWidth2,frameHeight2,GetSecondImagePoints)

            
            

            ang = math.degrees(math.atan2(FinalAnklePoints[1]-KneePoint[1], FinalAnklePoints[0]-KneePoint[0]) - math.atan2(InitialAnklePoints[1]-KneePoint[1], InitialAnklePoints[0]-KneePoint[0]))
            
            if ang < 0:
                ROM_1 =  ang + 360
            else:
                ROM_1 = ang
            
            print("Range Of Motion is ",int(ROM_1),"°")
            return int(ROM_1)

        
        def skeletonImage(path):
            ROM.videotoimageconverter(path)
            print("Taking the Initial and Fianl images \nSkeleton Images are being formed...")
            InitialOutput,FinalOutput,frameWidth1,frameHeight1,frameWidth2,frameHeight2,image1,image2 = ROM.readFrame(InitialimagePath,FinalimagePath)
            KneePoint = ROM.FetchingKneeKeypoint(18,InitialOutput,InitialimagePath)
            InitialAnklePoints = ROM.FetchingAnkleKeypoints(18,InitialOutput,InitialimagePath)
            FinalAnklePoints = ROM.FetchingAnkleKeypoints(18,FinalOutput,FinalimagePath)
            GetFirstImagePoints,FirstKeylist = ROM.GetImageKeypoints(18,InitialOutput,InitialimagePath)
            GetSecondImagePoints,SecondKeylist = ROM.GetImageKeypoints(18,FinalOutput,FinalimagePath)
            I_valid_pairs, I_invalid_pairs = ROM.getValidPairs(InitialOutput,frameWidth1,frameHeight1,GetFirstImagePoints)

            F_valid_pairs, F_invalid_pairs = ROM.getValidPairs(FinalOutput,frameWidth2,frameHeight2,GetSecondImagePoints)

            I_personwiseKeypoints = ROM.getPersonwiseKeypoints(I_valid_pairs, I_invalid_pairs,FirstKeylist)
            F_personwiseKeypoints = ROM.getPersonwiseKeypoints(F_valid_pairs, F_invalid_pairs,SecondKeylist)

            frameClone1 = image1.copy()

            for i in range(17):
                for n in range(len(I_personwiseKeypoints)):
                    index = I_personwiseKeypoints[n][np.array(POSE_PAIRS[i])]
                    if -1 in index:
                        continue
                    B = np.int32(FirstKeylist[index.astype(int), 0])
                    A = np.int32(FirstKeylist[index.astype(int), 1])
                    cv2.line(frameClone1, (B[0], A[0]), (B[1], A[1]), colors[i], 3, cv2.LINE_AA)

            plt.figure(figsize=[15,15])
            plt.imshow(frameClone1[:,:,[2,1,0]])
            plt.savefig('images/InitialFrame.png')


            frameClone2 = image2.copy()

            for i in range(17):
                for n in range(len(F_personwiseKeypoints)):
                    index = F_personwiseKeypoints[n][np.array(POSE_PAIRS[i])]
                    if -1 in index:
                        continue
                    B = np.int32(SecondKeylist[index.astype(int), 0])
                    A = np.int32(SecondKeylist[index.astype(int), 1])
                    cv2.line(frameClone2, (B[0], A[0]), (B[1], A[1]), colors[i], 3, cv2.LINE_AA)

            plt.figure(figsize=[15,15])
            plt.imshow(frameClone2[:,:,[2,1,0]])
            plt.savefig('images/FinalFrame.png')

            ImgPath1 = 'images/InitialFrame.png'
            ImgPath2 = 'images/FinalFrame.png'
            I_pic = Image.open(ImgPath1)
            F_pic = Image.open(ImgPath2)
            print("Skeleton images got saved sucessfully")

            return I_pic,F_pic