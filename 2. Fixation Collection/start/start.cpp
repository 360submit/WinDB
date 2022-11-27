#include "stdafx.h"
#include <tobii/tobii.h>
#include <tobii/tobii_streams.h>
#include <stdio.h>
#include <assert.h>
#include <string.h>
#include <iostream>
#include <string>
#include <time.h>
#include <opencv2/opencv.hpp>  
#include <vector>  
#include <io.h> 
#include <fstream>
#include <direct.h>
#include<windows.h>
#include<Mmsystem.h>
#pragma comment(lib,"winmm.lib")
#pragma warning(disable:4996)

using namespace cv;
using namespace std;

int pre = 0;
FILE* fp;
const char* img_name;
int smoothoff = 0;
int indexqx = 0, indexon;
double indexcx1, indexcx2, indexcx3, indexcx4, indexcx5, indexcx6, indexall1[] = { 10, 9,8,7,6,5,4,3,2,1 }, indexall2[] = { 30,29,28,27,26,25,24,23,22,21,20,19,18,17,16,15,14,13,12,11,10,9,8,7,6,5,4,3,2,1 };;//清晰的辅屏indexqx，模糊持续的时间indexcx
int indexallnum;
int indexgzl1 = 0, indexgzl2 = 0, indexgzl3 = 0, indexgzl4 = 0, indexgzl5 = 0, indexgzl6 = 0, indexgzl = 30;
int chosemy;
long float x, y;
string old_path, figname, fignames_path, fignames;
const double EPS = 0.0000001;

int start_nums = 0;
int end_nums = start_nums+30;
string peopleindex = "\\Peoplename.txt";

string filenameMy[300] = {"1","10","101","102","103","104-1","104-2","104-3","105","106","107","108","109","11-1","11-2","11-3","11-4","11-5","110","111","112","113","114","115","116","117","118","119","12","120","121","122","123","124","125","126","127","128","129","13","130","131","132","133-1","133-2","133-3","134","135","136","137","138","139","14","140","141","142","143","144","145","146","147","148","149","15","150","151","152","153","154","155","156","157","158","159","16","160","161","162","163","164","165","166","167","168","169","17","170","171","172","173","174","175","176","177-1","177-2","178","179","18","180","181","182","183","184","185","186","187","188","189","19-1","19-2","19-3","19-4","19-5","190","191","192","193","194","195","196","197","198","199","2","20-1","20-2","200","201","202","203","204","205","206","207","208","209","21","21-1","210","211","212","213","214","215","216","217","218","219","22","220","221","222","223","224","225","226","227","228","229","23","230","231","232","233","234","235","236","237","238","24","25-1","25-2","26","27","28","29-1","29-2","29-3","30","31-1","31-2","31-3","31-4","31-5","31-6","32-2","32-3","33","34","35","36","37","38","39","3_1","3_2","40","41","42","43","44","45","46","47","48","49","4_1","4_2","5","50","51-1","51-2","51-3","51-4","52","53","54","55-1","55-2","55-3","55-4","56-1","56-2","56-3","56-4","56-5","56-6","56-7","57","58","59","6","60","61-1","61-2","61-3","62","63","64","65-1","65-2","65-3","66","67-1","67-2","68-1","68-2","69-1","69-2","69-3","69-4","69-5","7","70-1","70-2","71","72","73","74","75","76-1","76-2","76-3","76-4","77-1","77-2","77-3","78","79","8","80-1","80-2","81-1","81-2","82","83-1","83-2","83-3","84","85","86","87","88-1","88-2","89-1","89-2","90","91-1","91-2","91-3","91-4","92-1","92-2","92-3","92-4","93","94-1","94-2","9_1","9_2" };
string getTime() {
	time_t timep;
	time(&timep);
	char tmp[64];
	strftime(tmp, sizeof(tmp), "%Y-%m-%d %H:%M:%S", localtime(&timep));
	return tmp;
}


LPCWSTR stringToLPCWSTR(std::string orig)
{
	size_t origsize = orig.length() + 1;
	const size_t newsize = 100;
	size_t convertedChars = 0;
	wchar_t* wcstring = (wchar_t*)malloc(sizeof(wchar_t) * (orig.length() - 1));
	mbstowcs_s(&convertedChars, wcstring, origsize, orig.c_str(), _TRUNCATE);

	return wcstring;
}

void gaze_point_callback(tobii_gaze_point_t const* gaze_point, void* user_data) {
	y = int(gaze_point->position_xy[0] * 1920 + 0.5);
	x = int(gaze_point->position_xy[1] * 1080 + 0.5);

	fprintf(fp, "%s %d %7.5lf %7.5lf\n", img_name, 0, y, x);
	if (x > 0 && x < 300 && y>0 && y < 640) {
		smoothoff = 1;
		indexqx = 1;
	}
	if (x > 0 && x < 300 && y>640 && y < 1280) {
		smoothoff = 1;
		indexqx = 2;
	}
	if (x > 0 && x < 300 && y>1280 && y < 1920) {
		smoothoff = 1;
		indexqx = 3;
	}

	if (x > 840 && x < 1080 && y>0 && y < 640) {
		smoothoff = 1;
		indexqx = 4;
	}
	if (x > 840 && x < 1080 && y>640 && y < 1280) {
		smoothoff = 1;
		indexqx = 5;
	}
	if (x > 840 && x < 1080 && y>1280 && y < 1920) {
		smoothoff = 1;
		indexqx = 6;
	}
	if (gaze_point->validity == TOBII_VALIDITY_VALID) {
		string time = getTime(); cout << time << endl;
		printf("Gaze point:%s, %f, %f \n", img_name, gaze_point->position_xy[0], gaze_point->position_xy[1]);
	}
}

void smooth_of_my(Mat& masksmoothh, Mat& masksmooth, double& indexcx, int& chosemy) {
	Mat masksmoothh_dst, masksmooth_dst;
	int ksize1 = 0;
	int ksize2 = 0;
	if (chosemy == 0) {
		double sigma1 = 3.1 - 0.3 * indexcx;
		double sigma2 = 3.1 - 0.3 * indexcx;
		GaussianBlur(masksmoothh, masksmoothh, Size(ksize1, ksize2), sigma1, sigma2);
		GaussianBlur(masksmooth, masksmooth, Size(ksize1, ksize2), sigma1, sigma2);
	}
	if (chosemy == 1) {
		double sigma1 = 3.1 - 0.1 * indexcx;
		double sigma2 = 3.1 - 0.1 * indexcx;
		GaussianBlur(masksmoothh, masksmoothh, Size(ksize1, ksize2), sigma1, sigma2);
		GaussianBlur(masksmooth, masksmooth, Size(ksize1, ksize2), sigma1, sigma2);
	}
}

bool valueFind(int on, double value) {
	bool bfind = false;
	if (on == 1) {
		for (int i = 0;i < 10;i++) {
			if (abs(indexall1[i] - value) < EPS) {
				bfind = true;
				break;
			}
		}
	}
	if (on == 2) {
		for (int i = 0;i < indexgzl;i++) {
			if (abs(indexall2[i] - value) < EPS) {
				bfind = true;
				break;
			}
		}
	}
	return bfind;
}

static void url_receiver(char const* url, void* user_data) {
	char* buffer = (char*)user_data;
	if (*buffer != '\0') return;

	if (strlen(url) < 256)
		strcpy(buffer, url);
}

int main(int argc, char** argv) {
	tobii_api_t* api;
	tobii_error_t error = tobii_api_create(&api, NULL, NULL);  assert(error == TOBII_ERROR_NO_ERROR);
	char url[256] = { 0 };
	error = tobii_enumerate_local_device_urls(api, url_receiver, url);  assert(error == TOBII_ERROR_NO_ERROR && *url != '\0');
	tobii_device_t* device;
	error = tobii_device_create(api, url, &device);  assert(error == TOBII_ERROR_NO_ERROR);
	error = tobii_gaze_point_subscribe(device, gaze_point_callback, 0);  assert(error == TOBII_ERROR_NO_ERROR);

	for (int filename_index = start_nums;filename_index < end_nums; filename_index++) {
		Mat temp, masksmoothh, masksmooth, roiImage;
		bool onoff;

		string txt_path = "\\PathSaveTxt\\" + filenameMy[filename_index];
		if (access(txt_path.c_str(), 0) == -1)
			mkdir(txt_path.c_str());
		if (access((txt_path + "\\" + peopleindex).c_str(), 0) == -1) {
			ofstream out_data;
			out_data.open((txt_path + "\\" + peopleindex), ios::app);
			out_data.close();
		}
		fp = fopen((txt_path + "\\" + peopleindex).c_str(), "w");
		if (fp == NULL)
			fprintf(stderr, "Can't open position.txt");

		string folder_path = "\\DataSet\\" + filenameMy[filename_index] + "\\*.jpg";
		vector<cv::String> file_names;
		glob(folder_path, file_names);

		//Mat img;
		temp = imread(file_names[0]);

		imshow("IMG", temp);
		namedWindow("IMG", CV_WINDOW_NORMAL);
		HWND win_handle = FindWindow(0, L"IMG");
		SetWindowLong(win_handle, GWL_STYLE, GetWindowLong(win_handle, GWL_EXSTYLE | WS_EX_TOPMOST));
		ShowWindow(win_handle, SW_SHOW);
		moveWindow("IMG", 1, 1);
		waitKey(1);

		for (int fig_i = 0; fig_i < file_names.size(); fig_i++) {
			img_name = (file_names[fig_i]).c_str();
			temp = imread(file_names[fig_i]);
			if(fig_i % 100 == 0){
				int lenstr = file_names[fig_i].length();int starstr = file_names[fig_i].rfind("\\") + 1; int endstr = lenstr - 4 - starstr;
				string wavname = file_names[fig_i].substr(starstr, endstr);
				string soundPath = "\\AudioDataPath\\" + filenameMy[filename_index] + "\\" + wavname + ".wav";
				PlaySound(stringToLPCWSTR(soundPath), NULL, SND_FILENAME | SND_ASYNC);
				cout << soundPath;
			}
			fignames = file_names[fig_i].substr(0, file_names[fig_i].length() - 4);

			if (smoothoff == 1) {
				if (indexqx == 1) {
					indexcx1 = 10;indexallnum = 10;
					fignames_path = fignames + "_1_0.png";
					masksmoothh = imread(fignames_path);
					masksmooth = imread(fignames_path, 0);
					chosemy = 0;
					indexon = 1;
					smooth_of_my(masksmoothh, masksmooth, indexcx1, chosemy);
					roiImage = temp(Rect(640 * 0, 0, 640, 240));
					masksmoothh.copyTo(roiImage, masksmooth);
					indexqx = 0;
					indexgzl1 = indexgzl1 + 1;
					if ((indexgzl1 - indexgzl) > 0) {
						indexcx1 = indexgzl - (indexgzl1 - indexgzl);
						chosemy = 1;indexallnum = 30;indexon = 2;
					}
				}
				if (valueFind(indexon, indexcx1)) {
					fignames_path = fignames + "_1_0.png";
					fignames_path = fignames + "_1_0.png";
					masksmoothh = imread(fignames_path);
					masksmooth = imread(fignames_path, 0);
					smooth_of_my(masksmoothh, masksmooth, indexcx1, chosemy);
					roiImage = temp(Rect(640 * 0, 0, 640, 240));
					masksmoothh.copyTo(roiImage, masksmooth);
					indexcx1 = indexcx1 - 1;
					if (indexcx1 - 1 < 0) indexgzl1 = 0;
				}
				if (indexqx == 2) {
					indexcx2 = 10;indexallnum = 10;
					fignames_path = fignames + "_1_1.png";
					masksmoothh = imread(fignames_path);
					masksmooth = imread(fignames_path, 0);
					chosemy = 0;
					indexon = 1;
					smooth_of_my(masksmoothh, masksmooth, indexcx2, chosemy);
					roiImage = temp(Rect(640 * 1, 0, 640, 240));
					masksmoothh.copyTo(roiImage, masksmooth);
					indexqx = 0;
					indexgzl2 = indexgzl2 + 1;
					if ((indexgzl2 - indexgzl) > 0) {
						indexcx2 = indexgzl - (indexgzl2 - indexgzl);
						chosemy = 1;indexallnum = 30;indexon = 2;
					}
				}
				if (valueFind(indexon, indexcx2)) {
					fignames_path = fignames + "_1_1.png";
					masksmoothh = imread(fignames_path);
					masksmooth = imread(fignames_path, 0);
					smooth_of_my(masksmoothh, masksmooth, indexcx2, chosemy);
					roiImage = temp(Rect(640 * 1, 0, 640, 240));
					masksmoothh.copyTo(roiImage, masksmooth);
					indexcx2 = indexcx2 - 1;
					if (indexcx2 - 1 < 0) indexgzl2 = 0;
				}
				if (indexqx == 3) {
					indexcx3 = 10;indexallnum = 10;
					fignames_path = fignames + "_1_2.png";
					masksmoothh = imread(fignames_path);
					masksmooth = imread(fignames_path, 0);
					chosemy = 0;
					indexon = 1;
					smooth_of_my(masksmoothh, masksmooth, indexcx3, chosemy);
					roiImage = temp(Rect(640 * 2, 0, 640, 240));
					masksmoothh.copyTo(roiImage, masksmooth);
					indexqx = 0;
					indexgzl3 = indexgzl3 + 1;
					if ((indexgzl3 - indexgzl) > 0) {
						indexcx3 = indexgzl - (indexgzl3 - indexgzl);
						chosemy = 1;indexallnum = 30;indexon = 2;
					}
				}
				if (valueFind(indexon, indexcx3)) {
					fignames_path = fignames + "_1_2.png";
					masksmoothh = imread(fignames_path);
					masksmooth = imread(fignames_path, 0);
					smooth_of_my(masksmoothh, masksmooth, indexcx3, chosemy);
					roiImage = temp(Rect(640 * 2, 0, 640, 240));
					masksmoothh.copyTo(roiImage, masksmooth);
					indexcx3 = indexcx3 - 1;
					if (indexcx3 - 1 < 0) indexgzl3 = 0;
				}



				if (indexqx == 4) {
					indexcx4 = 10;indexallnum = 10;
					fignames_path = fignames + "_2_0.png";
					masksmoothh = imread(fignames_path);
					masksmooth = imread(fignames_path, 0);
					chosemy = 0;indexon = 1;
					smooth_of_my(masksmoothh, masksmooth, indexcx4, chosemy);
					roiImage = temp(Rect(640 * 0, 1080 - 240, 640, 240));
					masksmoothh.copyTo(roiImage, masksmooth);
					indexqx = 0;
					indexgzl4 = indexgzl4 + 1;
					if ((indexgzl4 - indexgzl) > 0) {
						indexcx4 = indexgzl - (indexgzl4 - indexgzl);
						chosemy = 1;indexallnum = 30;indexon = 2;
					}
				}
				if (valueFind(indexon, indexcx4)) {
					fignames_path = fignames + "_2_0.png";
					masksmoothh = imread(fignames_path);
					masksmooth = imread(fignames_path, 0);
					smooth_of_my(masksmoothh, masksmooth, indexcx4, chosemy);
					roiImage = temp(Rect(640 * 0, 1080 - 240, 640, 240));
					masksmoothh.copyTo(roiImage, masksmooth);
					indexcx4 = indexcx4 - 1;
					if (indexcx4 - 1 < 0) indexgzl4 = 0;
				}
				if (indexqx == 5) {
					indexcx5 = 10;indexallnum = 10;
					fignames_path = fignames + "_2_1.png";
					masksmoothh = imread(fignames_path);
					masksmooth = imread(fignames_path, 0);
					chosemy = 0;indexon = 1;
					smooth_of_my(masksmoothh, masksmooth, indexcx5, chosemy);
					roiImage = temp(Rect(640 * 1, 1080 - 240, 640, 240));
					masksmoothh.copyTo(roiImage, masksmooth);
					indexqx = 0;
					indexgzl5 = indexgzl5 + 1;
					if ((indexgzl5 - indexgzl) > 0) {
						indexcx5 = indexgzl - (indexgzl5 - indexgzl);
						chosemy = 1;indexallnum = 30;indexon = 2;
					}
				}
				if (valueFind(indexon, indexcx5)) {
					fignames_path = fignames + "_2_1.png";
					masksmoothh = imread(fignames_path);
					masksmooth = imread(fignames_path, 0);
					smooth_of_my(masksmoothh, masksmooth, indexcx5, chosemy);
					roiImage = temp(Rect(640 * 1, 1080 - 240, 640, 240));
					masksmoothh.copyTo(roiImage, masksmooth);
					indexcx5 = indexcx5 - 1;
					if (indexcx5 - 1 < 0) indexgzl5 = 0;
				}
				if (indexqx == 6) {
					indexcx6 = 10;indexallnum = 10;
					fignames_path = fignames + "_2_2.png";
					masksmoothh = imread(fignames_path);
					masksmooth = imread(fignames_path, 0);
					chosemy = 0;indexon = 1;
					smooth_of_my(masksmoothh, masksmooth, indexcx6, chosemy);
					roiImage = temp(Rect(640 * 2, 1080 - 240, 640, 240));
					masksmoothh.copyTo(roiImage, masksmooth);
					indexqx = 0;
					indexgzl6 = indexgzl6 + 1;
					if ((indexgzl6 - indexgzl) > 0) {
						indexcx6 = indexgzl - (indexgzl6 - indexgzl);
						chosemy = 1;indexallnum = 30;indexon = 2;
					}
				}
				if (valueFind(indexon, indexcx6)) {
					fignames_path = fignames + "_2_2.png";
					masksmoothh = imread(fignames_path);
					masksmooth = imread(fignames_path, 0);
					smooth_of_my(masksmoothh, masksmooth, indexcx6, chosemy);
					roiImage = temp(Rect(640 * 2, 1080-240, 640, 240));
					masksmoothh.copyTo(roiImage, masksmooth);
					indexcx6 = indexcx6 - 1;
					if (indexcx6 - 1 < 0) indexgzl6 = 0;
				}

				imshow("IMG", temp);
				namedWindow("IMG", CV_WINDOW_NORMAL);
				HWND win_handle = FindWindow(0, L"IMG");
				SetWindowLong(win_handle, GWL_STYLE, GetWindowLong(win_handle, GWL_EXSTYLE | WS_EX_TOPMOST));
				ShowWindow(win_handle, SW_SHOW);
				moveWindow("IMG", 1, 1);
				waitKey(1);
			}
					
			int is_running = 3;
			while (--is_running >= 0) {
				error = tobii_wait_for_callbacks(NULL, 1, &device);	assert(error == TOBII_ERROR_NO_ERROR || error == TOBII_ERROR_TIMED_OUT);
				error = tobii_device_process_callbacks(device);		assert(error == TOBII_ERROR_NO_ERROR);
			}
		}
		fclose(fp);
	}
    
	error = tobii_gaze_point_unsubscribe(device);	assert(error == TOBII_ERROR_NO_ERROR);
	error = tobii_device_destroy(device);			assert(error == TOBII_ERROR_NO_ERROR);
	error = tobii_api_destroy(api);					assert(error == TOBII_ERROR_NO_ERROR);

	return 0;
}