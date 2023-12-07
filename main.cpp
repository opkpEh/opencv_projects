//Read the README for keyboard commands 

#include <opencv2/opencv.hpp>
#include <iostream>
#include <ctime>
#include <string>


int main()
{	
	cv::VideoCapture vid_cap(0);
	cv::Mat img;
	
	cv::VideoWriter video_writer;

	int frame_width = vid_cap.get(cv::CAP_PROP_FRAME_WIDTH);
	int frame_height = vid_cap.get(cv::CAP_PROP_FRAME_HEIGHT);

	while (true)
	{
		vid_cap.read(img);

		std::time_t t = std::time(0);

		cv::imshow("window", img);
		int key = cv::waitKey(1);  

		if (key == 'q' || key == 27)  
		{
			break;
		}
		
		else if (key == 32)
		{
			std::string fileName = std::to_string(t);
			fileName.append(".jpeg");
			cv::imwrite(fileName, img);
		}

		else if (key == 116)
		{
			std::string videoFileName = std::to_string(t);
			videoFileName.append(".avi");
			 video_writer.open(videoFileName, cv::VideoWriter::fourcc('M', 'J', 'P', 'G'), 32, cv::Size(frame_width, frame_height));

		}

		else if (key == 'y')
		{
			video_writer.release();
		}
		else if (video_writer.isOpened())
		{
			video_writer.write(img);
		}
	}

	return 0;
}
