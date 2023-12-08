//Read the README for keyboard commands 
#include <opencv2/opencv.hpp>
#include <iostream>
#include <ctime>
#include <string>
#include <raylib.h>

int main()
{	

	InitWindow(800,600,"Camera");

	cv::VideoCapture vid_cap(0); //open defualt camera
	cv::Mat img;	

	cv::VideoWriter video_writer;

	int frame_width = vid_cap.get(cv::CAP_PROP_FRAME_WIDTH);
	int frame_height = vid_cap.get(cv::CAP_PROP_FRAME_HEIGHT);

	if (!vid_cap.isOpened())
	{
		std::cout << "Failed to open web cam";
		return -1;
	}

	while (!WindowShouldClose())
	{
		//reading the image 
		vid_cap.read(img);

		//calcluating the time
		std::time_t t = std::time(0);

		//displaying the live feed 
		cv::imshow("CAMERA", img);
		int key = cv::waitKey(1);  

		//Making raylib camera work
		BeginDrawing();
		ClearBackground(RAYWHITE);

		//cv::cvtColor(img, img, cv::COLOR_BGR2RGB);
		
		//Image image= LoadImage(img.data, img.rows, img.cols, PIXELFORMAT_UNCOMPRESSED_R8G8B8A8);
		//Texture2D texture = LoadTextureFromImage(image);
		//DrawTexture(texture, 0, 0, WHITE);

		EndDrawing();

		//stoping the code
		if (key == 'q' || key == 27)  
		{
			std::cout << "Camera Closed" << std::endl;
			break;
		}
		
		//take img and saivng it 
		else if (key == 32)
		{
			std::string fileName = std::to_string(t);
			fileName.append(".jpeg");

			cv::imwrite(fileName, img);
			std::cout << "Photo taken" << std::endl;
		}

		//starting video recording
		else if (key == 't')
		{
			std::string videoFileName = std::to_string(t);
			videoFileName.append(".avi");

			video_writer.open(videoFileName, cv::VideoWriter::fourcc('M', 'J', 'P', 'G'), 32, cv::Size(frame_width, frame_height));
			std::cout << "Recording started" << std::endl;
		}
		
		//stopping video recording
		else if (key == 'y')
		{
			video_writer.release();
			std::cout << "Recording ended" << std::endl;
		}

		//contuning video recording
		else if (video_writer.isOpened())
		{
			video_writer.write(img);
		}
	}

	return 0;
}
