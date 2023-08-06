#pragma once

#include <iostream>
#include <memory>
#include <string>
#include <list>
#include <map>
#include <thread>
#include <chrono>
#include <functional>

#include "rapidjson/document.h"
#include "rapidjson/writer.h"
#include "rapidjson/stringbuffer.h"
using namespace rapidjson;


class DalBaseUnitGRPC;


typedef std::function<std::string()> IF_Info;
typedef std::function<std::string(std::string,std::string)> IF_Meta;
typedef std::function<std::string(std::string, std::string)> IF_Data;
typedef std::function<std::string()> IF_NewData;

//#ifdef _MSC_VER
//class  _declspec(dllimport) DalBaseUnit {
//#else 
//class   DalBaseUnit {
//#endif
class  DalBaseUnit {
public:
	bool inprocess = false;
	std::string s_dataIF;
	std::list<std::thread> list_threads;
	Document dicMethod; // ������Ǻ�������Ϊ��������ֵΪ������ָ��
	void pushIF_Info();
	

public:
	std::map<std::string, IF_Info> map_IFInfo; // ���溯�����ͺ�����ָ�룬����Ϊ�丳ֵ��
	std::map<std::string, IF_Meta> map_IFMeta; // ���溯�����ͺ�����ָ�룬����Ϊ�丳ֵ��
	std::map<std::string, IF_Data> map_IFData; // ���溯�����ͺ�����ָ�룬����Ϊ�丳ֵ��
	std::map<std::string, IF_NewData> map_IFNewData; // ���溯�����ͺ�����ָ�룬����Ϊ�丳ֵ��
	void logError();
	void logWarn();
	void logInfo();
	void quit();
	void start_frame();
	void run_new_data(IF_NewData p_if_newdata);
	static void newdata(std::string string_dicMeta, std::string string_dicData);
	static std::string Document2String(Document& documentin);
	static std::string Value2String(Value& valuein);
	std::string BindRequest(std::string s_request);
	

	DalBaseUnit();
	~DalBaseUnit();

	DalBaseUnitGRPC *m_pGRPC ;

	void run();
};