# coding: utf-8
"""GENERATED FILE. DO NOT EDIT."""
from __future__ import division, absolute_import, print_function, unicode_literals
from builtins import *

from ctypes import *
from copy import copy
from enum import Enum

from . import message_pb2 as tecrpc
from ..constant import *

class ValueType(Enum):
    Scalar = 0
    Array = 1
    Text = 2
    ArbParam = 3
    Address = 4


def try_cast_to_enum(EnumType, value):
    try:
        return EnumType(value)
    except ValueError:
        return None


class TecUtilRPC(object):

 def AddOnAllowUnload(self,add_on_id,do_allow_unload):
  args=((ValueType.Address,c_uint64,getattr(add_on_id,'value',add_on_id)),
        (ValueType.Scalar,c_bool,do_allow_unload),)
  rep=self.sndrcv("AddOnAllowUnload",*args)
  self.chk(rep)
 def AddOnGetPath(self,add_on_id):
  args=((ValueType.Address,c_uint64,getattr(add_on_id,'value',add_on_id)),)
  rep=self.sndrcv("AddOnGetPath",*args)
  self.chk(rep)
  return self.read_text(rep.args[0])
 def AddOnGetRegisteredInfo(self,official_name):
  args=((ValueType.Text,None,official_name),)
  rep=self.sndrcv("AddOnGetRegisteredInfo",*args)
  self.chk(rep)
  return (
   (rep.status == tecrpc.Reply.Success),
   self.read_text(rep.args[0]),
   self.read_text(rep.args[1]))
 def AddOnLoad(self,lib_name,not_used,not_used2):
  args=((ValueType.Text,None,lib_name),
        (ValueType.Text,None,not_used),
        (ValueType.Scalar,c_int32,not_used2),)
  rep=self.sndrcv("AddOnLoad",*args)
  self.chk(rep)
  return (rep.status == tecrpc.Reply.Success)
 def AddOnRegForeignLibLoader(self,foreign_lib_id,foreign_lib_loader,client_data):
  args=((ValueType.Text,None,foreign_lib_id),
        (ValueType.Address,c_uint64,getattr(foreign_lib_loader,'value',foreign_lib_loader)),
        (ValueType.ArbParam,None,client_data),)
  rep=self.sndrcv("AddOnRegForeignLibLoader",*args)
  self.chk(rep)
 def AddOnRegister(self,tecplot_base_version_number,official_name,version,author):
  args=((ValueType.Scalar,c_int32,tecplot_base_version_number),
        (ValueType.Text,None,official_name),
        (ValueType.Text,None,version),
        (ValueType.Text,None,author),)
  rep=self.sndrcv("AddOnRegister",*args)
  self.chk(rep)
  return rep.args[0].uint64
 def AddPreWriteLayoutCallback(self,write_layout_pre_write_callback,client_data):
  args=((ValueType.Address,c_uint64,getattr(write_layout_pre_write_callback,'value',write_layout_pre_write_callback)),
        (ValueType.ArbParam,None,client_data),)
  rep=self.sndrcv("AddPreWriteLayoutCallback",*args)
  self.chk(rep)
  return (rep.status == tecrpc.Reply.Success)
 def AnimateContourLevels(self,start_level,end_level,level_skip,create_movie_file,movie_f_name):
  args=((ValueType.Scalar,c_int32,start_level),
        (ValueType.Scalar,c_int32,end_level),
        (ValueType.Scalar,c_int32,level_skip),
        (ValueType.Scalar,c_bool,create_movie_file),
        (ValueType.Text,None,movie_f_name),)
  rep=self.sndrcv("AnimateContourLevels",*args)
  self.chk(rep)
  return (rep.status == tecrpc.Reply.Success)
 def AnimateContourLevelsX(self,arg_list):
  args=((ValueType.Address,c_uint64,getattr(arg_list,'value',arg_list)),)
  rep=self.sndrcv("AnimateContourLevelsX",*args)
  self.chk(rep)
  return (rep.status == tecrpc.Reply.Success)
 def AnimateIJKBlanking(self,start_i_min_fract,start_j_min_fract,start_k_min_fract,start_i_max_fract,start_j_max_fract,start_k_max_fract,end_i_min_fract,end_j_min_fract,end_k_min_fract,end_i_max_fract,end_j_max_fract,end_k_max_fract,num_steps,create_movie_file,movie_f_name):
  args=((ValueType.Scalar,c_double,start_i_min_fract),
        (ValueType.Scalar,c_double,start_j_min_fract),
        (ValueType.Scalar,c_double,start_k_min_fract),
        (ValueType.Scalar,c_double,start_i_max_fract),
        (ValueType.Scalar,c_double,start_j_max_fract),
        (ValueType.Scalar,c_double,start_k_max_fract),
        (ValueType.Scalar,c_double,end_i_min_fract),
        (ValueType.Scalar,c_double,end_j_min_fract),
        (ValueType.Scalar,c_double,end_k_min_fract),
        (ValueType.Scalar,c_double,end_i_max_fract),
        (ValueType.Scalar,c_double,end_j_max_fract),
        (ValueType.Scalar,c_double,end_k_max_fract),
        (ValueType.Scalar,c_int32,num_steps),
        (ValueType.Scalar,c_bool,create_movie_file),
        (ValueType.Text,None,movie_f_name),)
  rep=self.sndrcv("AnimateIJKBlanking",*args)
  self.chk(rep)
  return (rep.status == tecrpc.Reply.Success)
 def AnimateIJKBlankingX(self,arg_list):
  args=((ValueType.Address,c_uint64,getattr(arg_list,'value',arg_list)),)
  rep=self.sndrcv("AnimateIJKBlankingX",*args)
  self.chk(rep)
  return (rep.status == tecrpc.Reply.Success)
 def AnimateIJKPlanes(self,ij_or_k,start_index,end_index,index_skip,create_movie_file,movie_f_name):
  args=((ValueType.Text,None,ij_or_k),
        (ValueType.Scalar,c_int64,start_index),
        (ValueType.Scalar,c_int64,end_index),
        (ValueType.Scalar,c_int64,index_skip),
        (ValueType.Scalar,c_bool,create_movie_file),
        (ValueType.Text,None,movie_f_name),)
  rep=self.sndrcv("AnimateIJKPlanes",*args)
  self.chk(rep)
  return (rep.status == tecrpc.Reply.Success)
 def AnimateIJKPlanesX(self,arg_list):
  args=((ValueType.Address,c_uint64,getattr(arg_list,'value',arg_list)),)
  rep=self.sndrcv("AnimateIJKPlanesX",*args)
  self.chk(rep)
  return (rep.status == tecrpc.Reply.Success)
 def AnimateIsoSurfacesX(self,arg_list):
  args=((ValueType.Address,c_uint64,getattr(arg_list,'value',arg_list)),)
  rep=self.sndrcv("AnimateIsoSurfacesX",*args)
  self.chk(rep)
  return (rep.status == tecrpc.Reply.Success)
 def AnimateLineMapsX(self,arg_list):
  args=((ValueType.Address,c_uint64,getattr(arg_list,'value',arg_list)),)
  rep=self.sndrcv("AnimateLineMapsX",*args)
  self.chk(rep)
  return (rep.status == tecrpc.Reply.Success)
 def AnimateSlices(self,start_slice,end_slice,num_slices,create_movie_file,movie_f_name):
  args=((ValueType.Scalar,c_int32,start_slice),
        (ValueType.Scalar,c_int32,end_slice),
        (ValueType.Scalar,c_int32,num_slices),
        (ValueType.Scalar,c_bool,create_movie_file),
        (ValueType.Text,None,movie_f_name),)
  rep=self.sndrcv("AnimateSlices",*args)
  self.chk(rep)
  return (rep.status == tecrpc.Reply.Success)
 def AnimateSlicesX(self,arg_list):
  args=((ValueType.Address,c_uint64,getattr(arg_list,'value',arg_list)),)
  rep=self.sndrcv("AnimateSlicesX",*args)
  self.chk(rep)
  return (rep.status == tecrpc.Reply.Success)
 def AnimateStream(self,num_steps_per_cycle,num_cycles,create_movie_file,movie_f_name):
  args=((ValueType.Scalar,c_int32,num_steps_per_cycle),
        (ValueType.Scalar,c_int32,num_cycles),
        (ValueType.Scalar,c_bool,create_movie_file),
        (ValueType.Text,None,movie_f_name),)
  rep=self.sndrcv("AnimateStream",*args)
  self.chk(rep)
  return (rep.status == tecrpc.Reply.Success)
 def AnimateStreamX(self,arg_list):
  args=((ValueType.Address,c_uint64,getattr(arg_list,'value',arg_list)),)
  rep=self.sndrcv("AnimateStreamX",*args)
  self.chk(rep)
  return (rep.status == tecrpc.Reply.Success)
 def AnimateTimeX(self,arg_list):
  args=((ValueType.Address,c_uint64,getattr(arg_list,'value',arg_list)),)
  rep=self.sndrcv("AnimateTimeX",*args)
  self.chk(rep)
  return (rep.status == tecrpc.Reply.Success)
 def AnimateZones(self,start_zone,end_zone,zone_skip,create_movie_file,movie_f_name):
  args=((ValueType.Scalar,c_int32,start_zone),
        (ValueType.Scalar,c_int32,end_zone),
        (ValueType.Scalar,c_int32,zone_skip),
        (ValueType.Scalar,c_bool,create_movie_file),
        (ValueType.Text,None,movie_f_name),)
  rep=self.sndrcv("AnimateZones",*args)
  self.chk(rep)
  return (rep.status == tecrpc.Reply.Success)
 def AnimateZonesX(self,arg_list):
  args=((ValueType.Address,c_uint64,getattr(arg_list,'value',arg_list)),)
  rep=self.sndrcv("AnimateZonesX",*args)
  self.chk(rep)
  return (rep.status == tecrpc.Reply.Success)
 def AnimationIsSequencedExportFormat(self,export_format):
  args=((ValueType.Scalar,c_int32,ExportFormat(export_format).value),)
  rep=self.sndrcv("AnimationIsSequencedExportFormat",*args)
  self.chk(rep)
  return (rep.status == tecrpc.Reply.Success)
 def ArgListAlloc(self):
  rep=self.sndrcv("ArgListAlloc")
  self.chk(rep)
  return rep.args[0].uint64
 def ArgListAppendArbParam(self,arg_list,name,value):
  args=((ValueType.Address,c_uint64,getattr(arg_list,'value',arg_list)),
        (ValueType.Text,None,name),
        (ValueType.ArbParam,None,value),)
  rep=self.sndrcv("ArgListAppendArbParam",*args)
  self.chk(rep)
  return (rep.status == tecrpc.Reply.Success)
 def ArgListAppendArbParamPtr(self,arg_list,name,value):
  args=((ValueType.Address,c_uint64,getattr(arg_list,'value',arg_list)),
        (ValueType.Text,None,name),
        (ValueType.ArbParam,None,value.contents),)
  rep=self.sndrcv("ArgListAppendArbParamPtr",*args)
  self.chk(rep)
  return (rep.status == tecrpc.Reply.Success)
 def ArgListAppendArray(self,arg_list,name,value):
  args=((ValueType.Address,c_uint64,getattr(arg_list,'value',arg_list)),
        (ValueType.Text,None,name),
        (ValueType.Array,c_uint8,value),)
  rep=self.sndrcv("ArgListAppendArray",*args)
  self.chk(rep)
  return (rep.status == tecrpc.Reply.Success)
 def ArgListAppendDouble(self,arg_list,name,value):
  args=((ValueType.Address,c_uint64,getattr(arg_list,'value',arg_list)),
        (ValueType.Text,None,name),
        (ValueType.Scalar,c_double,value),)
  rep=self.sndrcv("ArgListAppendDouble",*args)
  self.chk(rep)
  return (rep.status == tecrpc.Reply.Success)
 def ArgListAppendDoublePtr(self,arg_list,name,value):
  args=((ValueType.Address,c_uint64,getattr(arg_list,'value',arg_list)),
        (ValueType.Text,None,name),
        (ValueType.Scalar,c_double,value.contents.value),)
  rep=self.sndrcv("ArgListAppendDoublePtr",*args)
  self.chk(rep)
  return (rep.status == tecrpc.Reply.Success)
 def ArgListAppendFunction(self,arg_list,name,value):
  args=((ValueType.Address,c_uint64,getattr(arg_list,'value',arg_list)),
        (ValueType.Text,None,name),
        (ValueType.Address,c_uint64,value.contents.value),)
  rep=self.sndrcv("ArgListAppendFunction",*args)
  self.chk(rep)
  return (rep.status == tecrpc.Reply.Success)
 def ArgListAppendInt(self,arg_list,name,value):
  args=((ValueType.Address,c_uint64,getattr(arg_list,'value',arg_list)),
        (ValueType.Text,None,name),
        (ValueType.Scalar,c_int64,value),)
  rep=self.sndrcv("ArgListAppendInt",*args)
  self.chk(rep)
  return (rep.status == tecrpc.Reply.Success)
 def ArgListAppendSet(self,arg_list,name,value):
  args=((ValueType.Address,c_uint64,getattr(arg_list,'value',arg_list)),
        (ValueType.Text,None,name),
        (ValueType.Address,c_uint64,getattr(value,'value',value)),)
  rep=self.sndrcv("ArgListAppendSet",*args)
  self.chk(rep)
  return (rep.status == tecrpc.Reply.Success)
 def ArgListAppendString(self,arg_list,name,value):
  args=((ValueType.Address,c_uint64,getattr(arg_list,'value',arg_list)),
        (ValueType.Text,None,name),
        (ValueType.Text,None,value),)
  rep=self.sndrcv("ArgListAppendString",*args)
  self.chk(rep)
  return (rep.status == tecrpc.Reply.Success)
 def ArgListAppendStringList(self,arg_list,name,string_list):
  args=((ValueType.Address,c_uint64,getattr(arg_list,'value',arg_list)),
        (ValueType.Text,None,name),
        (ValueType.Address,c_uint64,getattr(string_list,'value',string_list)),)
  rep=self.sndrcv("ArgListAppendStringList",*args)
  self.chk(rep)
  return (rep.status == tecrpc.Reply.Success)
 def ArgListAppendStringPtr(self,arg_list,name,value):
  args=((ValueType.Address,c_uint64,getattr(arg_list,'value',arg_list)),
        (ValueType.Text,None,name),
        (ValueType.Address,c_uint64,value.contents.value),)
  rep=self.sndrcv("ArgListAppendStringPtr",*args)
  self.chk(rep)
  return (rep.status == tecrpc.Reply.Success)
 def ArgListClear(self,arg_list):
  args=((ValueType.Address,c_uint64,getattr(arg_list,'value',arg_list)),)
  rep=self.sndrcv("ArgListClear",*args)
  self.chk(rep)
 def ArgListDealloc(self,arg_list):
  args=((ValueType.Address,c_uint64,arg_list.contents.value),)
  rep=self.sndrcv("ArgListDealloc",*args)
  self.chk(rep)
  return rep.args[0].uint64
 def ArgListGetArbParamByIndex(self,arg_list,index):
  args=((ValueType.Address,c_uint64,getattr(arg_list,'value',arg_list)),
        (ValueType.Scalar,c_int32,index),)
  rep=self.sndrcv("ArgListGetArbParamByIndex",*args)
  self.chk(rep)
  return self.read_arbparam(rep.args[0])
 def ArgListGetArbParamPtrByIndex(self,arg_list,index):
  args=((ValueType.Address,c_uint64,getattr(arg_list,'value',arg_list)),
        (ValueType.Scalar,c_int32,index),)
  rep=self.sndrcv("ArgListGetArbParamPtrByIndex",*args)
  self.chk(rep)
  ret = arg_list._handles[index - 1]
  ret[0] = self.read_arbparam(rep.args[0])
  return ret
 def ArgListGetArgCount(self,arg_list):
  args=((ValueType.Address,c_uint64,getattr(arg_list,'value',arg_list)),)
  rep=self.sndrcv("ArgListGetArgCount",*args)
  self.chk(rep)
  return rep.args[0].int32
 def ArgListGetArgNameByIndex(self,arg_list,index):
  args=((ValueType.Address,c_uint64,getattr(arg_list,'value',arg_list)),
        (ValueType.Scalar,c_int32,index),)
  rep=self.sndrcv("ArgListGetArgNameByIndex",*args)
  self.chk(rep)
  return self.read_text(rep.args[0])
 def ArgListGetArgTypeByIndex(self,arg_list,index):
  args=((ValueType.Address,c_uint64,getattr(arg_list,'value',arg_list)),
        (ValueType.Scalar,c_int32,index),)
  rep=self.sndrcv("ArgListGetArgTypeByIndex",*args)
  self.chk(rep)
  return try_cast_to_enum(ArgListArgType, rep.args[0].int32)
 def ArgListGetArrayByIndex(self,arg_list,index):
  args=((ValueType.Address,c_uint64,getattr(arg_list,'value',arg_list)),
        (ValueType.Scalar,c_int32,index),)
  rep=self.sndrcv("ArgListGetArrayByIndex",*args)
  self.chk(rep)
  return rep.args[0].buffer
 def ArgListGetDoubleByIndex(self,arg_list,index):
  args=((ValueType.Address,c_uint64,getattr(arg_list,'value',arg_list)),
        (ValueType.Scalar,c_int32,index),)
  rep=self.sndrcv("ArgListGetDoubleByIndex",*args)
  self.chk(rep)
  return rep.args[0].float64
 def ArgListGetDoublePtrByIndex(self,arg_list,index):
  args=((ValueType.Address,c_uint64,getattr(arg_list,'value',arg_list)),
        (ValueType.Scalar,c_int32,index),)
  rep=self.sndrcv("ArgListGetDoublePtrByIndex",*args)
  self.chk(rep)
  ret = arg_list._handles[index - 1]
  ret[0] = rep.args[0].float64
  return ret
 def ArgListGetFunctionByIndex(self,arg_list,index):
  args=((ValueType.Address,c_uint64,getattr(arg_list,'value',arg_list)),
        (ValueType.Scalar,c_int32,index),)
  rep=self.sndrcv("ArgListGetFunctionByIndex",*args)
  self.chk(rep)
  return rep.args[0].buffer
 def ArgListGetIndexByArgName(self,arg_list,name):
  args=((ValueType.Address,c_uint64,getattr(arg_list,'value',arg_list)),
        (ValueType.Text,None,name),)
  rep=self.sndrcv("ArgListGetIndexByArgName",*args)
  self.chk(rep)
  return (
   (rep.status == tecrpc.Reply.Success),
   rep.args[0].int32)
 def ArgListGetIntByIndex(self,arg_list,index):
  args=((ValueType.Address,c_uint64,getattr(arg_list,'value',arg_list)),
        (ValueType.Scalar,c_int32,index),)
  rep=self.sndrcv("ArgListGetIntByIndex",*args)
  self.chk(rep)
  return rep.args[0].int32
 def ArgListGetSetByIndex(self,arg_list,index):
  args=((ValueType.Address,c_uint64,getattr(arg_list,'value',arg_list)),
        (ValueType.Scalar,c_int32,index),)
  rep=self.sndrcv("ArgListGetSetByIndex",*args)
  self.chk(rep)
  return rep.args[0].uint64
 def ArgListGetStringByIndex(self,arg_list,index):
  args=((ValueType.Address,c_uint64,getattr(arg_list,'value',arg_list)),
        (ValueType.Scalar,c_int32,index),)
  rep=self.sndrcv("ArgListGetStringByIndex",*args)
  self.chk(rep)
  return self.read_text(rep.args[0])
 def ArgListGetStringListByIndex(self,arg_list,index):
  args=((ValueType.Address,c_uint64,getattr(arg_list,'value',arg_list)),
        (ValueType.Scalar,c_int32,index),)
  rep=self.sndrcv("ArgListGetStringListByIndex",*args)
  self.chk(rep)
  return rep.args[0].uint64
 def ArrayAlloc(self,size,debug_info):
  args=((ValueType.Scalar,c_int64,size),
        (ValueType.Text,None,debug_info),)
  rep=self.sndrcv("ArrayAlloc",*args)
  self.chk(rep)
  return self.rep.args[0].uint64
 def ArrayDealloc(self,array):
  args=((ValueType.Address,c_uint64,array.contents.value),)
  rep=self.sndrcv("ArrayDealloc",*args)
  self.chk(rep)
  return rep.args[0].uint64
 def AutoRedrawIsActive(self):
  rep=self.sndrcv("AutoRedrawIsActive")
  self.chk(rep)
  return rep.args[0].boolean
 def AuxDataBeginAssign(self):
  rep=self.sndrcv("AuxDataBeginAssign")
  self.chk(rep)
 def AuxDataDataSetGetRef(self):
  rep=self.sndrcv("AuxDataDataSetGetRef")
  self.chk(rep)
  return rep.args[0].uint64
 def AuxDataDealloc(self,aux_data):
  args=((ValueType.Address,c_uint64,aux_data.contents.value),)
  rep=self.sndrcv("AuxDataDealloc",*args)
  self.chk(rep)
 def AuxDataDeleteItemByIndex(self,aux_data_ref,index):
  args=((ValueType.Address,c_uint64,getattr(aux_data_ref,'value',aux_data_ref)),
        (ValueType.Scalar,c_int32,index),)
  rep=self.sndrcv("AuxDataDeleteItemByIndex",*args)
  self.chk(rep)
 def AuxDataDeleteItemByName(self,aux_data_ref,name):
  args=((ValueType.Address,c_uint64,getattr(aux_data_ref,'value',aux_data_ref)),
        (ValueType.Text,None,name),)
  rep=self.sndrcv("AuxDataDeleteItemByName",*args)
  self.chk(rep)
  return (rep.status == tecrpc.Reply.Success)
 def AuxDataEndAssign(self):
  rep=self.sndrcv("AuxDataEndAssign")
  self.chk(rep)
 def AuxDataFrameGetRef(self):
  rep=self.sndrcv("AuxDataFrameGetRef")
  self.chk(rep)
  return rep.args[0].uint64
 def AuxDataGetItemByIndex(self,aux_data_ref,index):
  args=((ValueType.Address,c_uint64,getattr(aux_data_ref,'value',aux_data_ref)),
        (ValueType.Scalar,c_int32,index),)
  rep=self.sndrcv("AuxDataGetItemByIndex",*args)
  self.chk(rep)
  return (
   self.read_text(rep.args[0]),
   self.read_arbparam(rep.args[1]),
   try_cast_to_enum(AuxDataType, rep.args[2].int32),
   rep.args[3].boolean)
 def AuxDataGetItemByName(self,aux_data_ref,name):
  args=((ValueType.Address,c_uint64,getattr(aux_data_ref,'value',aux_data_ref)),
        (ValueType.Text,None,name),)
  rep=self.sndrcv("AuxDataGetItemByName",*args)
  self.chk(rep)
  return (
   (rep.status == tecrpc.Reply.Success),
   self.read_arbparam(rep.args[0]),
   try_cast_to_enum(AuxDataType, rep.args[1].int32),
   rep.args[2].boolean)
 def AuxDataGetItemIndex(self,aux_data_ref,name):
  args=((ValueType.Address,c_uint64,getattr(aux_data_ref,'value',aux_data_ref)),
        (ValueType.Text,None,name),)
  rep=self.sndrcv("AuxDataGetItemIndex",*args)
  self.chk(rep)
  return (
   (rep.status == tecrpc.Reply.Success),
   rep.args[0].int32)
 def AuxDataGetNumItems(self,aux_data_ref):
  args=((ValueType.Address,c_uint64,getattr(aux_data_ref,'value',aux_data_ref)),)
  rep=self.sndrcv("AuxDataGetNumItems",*args)
  self.chk(rep)
  return rep.args[0].int32
 def AuxDataGetStrItemByIndex(self,aux_data_ref,index):
  args=((ValueType.Address,c_uint64,getattr(aux_data_ref,'value',aux_data_ref)),
        (ValueType.Scalar,c_int32,index),)
  rep=self.sndrcv("AuxDataGetStrItemByIndex",*args)
  self.chk(rep)
  return (
   self.read_text(rep.args[0]),
   self.read_text(rep.args[1]),
   rep.args[2].boolean)
 def AuxDataGetStrItemByName(self,aux_data_ref,name):
  args=((ValueType.Address,c_uint64,getattr(aux_data_ref,'value',aux_data_ref)),
        (ValueType.Text,None,name),)
  rep=self.sndrcv("AuxDataGetStrItemByName",*args)
  self.chk(rep)
  return (
   (rep.status == tecrpc.Reply.Success),
   self.read_text(rep.args[0]),
   rep.args[1].boolean)
 def AuxDataLayoutGetRef(self):
  rep=self.sndrcv("AuxDataLayoutGetRef")
  self.chk(rep)
  return rep.args[0].uint64
 def AuxDataLineMapGetRef(self,map):
  args=((ValueType.Scalar,c_int32,map),)
  rep=self.sndrcv("AuxDataLineMapGetRef",*args)
  self.chk(rep)
  return rep.args[0].uint64
 def AuxDataPageGetRef(self):
  rep=self.sndrcv("AuxDataPageGetRef")
  self.chk(rep)
  return rep.args[0].uint64
 def AuxDataSetItem(self,aux_data_ref,name,value,type,retain):
  args=((ValueType.Address,c_uint64,getattr(aux_data_ref,'value',aux_data_ref)),
        (ValueType.Text,None,name),
        (ValueType.ArbParam,None,value),
        (ValueType.Scalar,c_int32,AuxDataType(type).value),
        (ValueType.Scalar,c_bool,retain),)
  rep=self.sndrcv("AuxDataSetItem",*args)
  self.chk(rep)
  return (rep.status == tecrpc.Reply.Success)
 def AuxDataSetStrItem(self,aux_data_ref,name,value,retain):
  args=((ValueType.Address,c_uint64,getattr(aux_data_ref,'value',aux_data_ref)),
        (ValueType.Text,None,name),
        (ValueType.Text,None,value),
        (ValueType.Scalar,c_bool,retain),)
  rep=self.sndrcv("AuxDataSetStrItem",*args)
  self.chk(rep)
  return (rep.status == tecrpc.Reply.Success)
 def AuxDataVarGetRef(self,var):
  args=((ValueType.Scalar,c_int32,var),)
  rep=self.sndrcv("AuxDataVarGetRef",*args)
  self.chk(rep)
  return rep.args[0].uint64
 def AuxDataZoneGetRef(self,zone):
  args=((ValueType.Scalar,c_int32,zone),)
  rep=self.sndrcv("AuxDataZoneGetRef",*args)
  self.chk(rep)
  return rep.args[0].uint64
 def AverageCellCenterData(self,zone_set,var_set):
  args=((ValueType.Address,c_uint64,getattr(zone_set,'value',zone_set)),
        (ValueType.Address,c_uint64,getattr(var_set,'value',var_set)),)
  rep=self.sndrcv("AverageCellCenterData",*args)
  self.chk(rep)
  return (rep.status == tecrpc.Reply.Success)
 def AxisGetGridRange(self):
  rep=self.sndrcv("AxisGetGridRange")
  self.chk(rep)
  return (
   (rep.status == tecrpc.Reply.Success),
   rep.args[0].float64,
   rep.args[1].float64,
   rep.args[2].float64,
   rep.args[3].float64)
 def AxisGetNextRangeValue(self,axis,axis_num,current_value,is_increasing,auto_adjust_to_nice_values):
  args=((ValueType.Text,None,axis),
        (ValueType.Scalar,c_int32,axis_num),
        (ValueType.Scalar,c_double,current_value),
        (ValueType.Scalar,c_bool,is_increasing),
        (ValueType.Scalar,c_bool,auto_adjust_to_nice_values),)
  rep=self.sndrcv("AxisGetNextRangeValue",*args)
  self.chk(rep)
  return rep.args[0].float64
 def AxisGetRange(self,axis,axis_num):
  args=((ValueType.Text,None,axis),
        (ValueType.Scalar,c_int32,axis_num),)
  rep=self.sndrcv("AxisGetRange",*args)
  self.chk(rep)
  return (
   rep.args[0].float64,
   rep.args[1].float64)
 def AxisGetVarAssignments(self):
  rep=self.sndrcv("AxisGetVarAssignments")
  self.chk(rep)
  return (
   rep.args[0].int32,
   rep.args[1].int32,
   rep.args[2].int32)
 def AxisLabelGetNumberFormat(self,axis,axis_num):
  args=((ValueType.Text,None,axis),
        (ValueType.Scalar,c_int32,axis_num),)
  rep=self.sndrcv("AxisLabelGetNumberFormat",*args)
  self.chk(rep)
  return try_cast_to_enum(NumberFormat, rep.args[0].int32)
 def AxisLabelGetPrecisionFormat(self,axis,axis_num):
  args=((ValueType.Text,None,axis),
        (ValueType.Scalar,c_int32,axis_num),)
  rep=self.sndrcv("AxisLabelGetPrecisionFormat",*args)
  self.chk(rep)
  return rep.args[0].int32
 def AxisLabelGetTimeDateFormat(self,axis,axis_num):
  args=((ValueType.Text,None,axis),
        (ValueType.Scalar,c_int32,axis_num),)
  rep=self.sndrcv("AxisLabelGetTimeDateFormat",*args)
  self.chk(rep)
  return self.read_text(rep.args[0])
 def BlankingCheckDataPoint(self,zone,point_index):
  args=((ValueType.Scalar,c_int32,zone),
        (ValueType.Scalar,c_int64,point_index),)
  rep=self.sndrcv("BlankingCheckDataPoint",*args)
  self.chk(rep)
  return rep.args[0].boolean
 def BlankingCheckFECell(self,zone,cell_index):
  args=((ValueType.Scalar,c_int32,zone),
        (ValueType.Scalar,c_int64,cell_index),)
  rep=self.sndrcv("BlankingCheckFECell",*args)
  self.chk(rep)
  return rep.args[0].boolean
 def BlankingCheckIJKCell(self,zone,zone_plane,cell_index):
  args=((ValueType.Scalar,c_int32,zone),
        (ValueType.Scalar,c_int32,IJKPlanes(zone_plane).value),
        (ValueType.Scalar,c_int64,cell_index),)
  rep=self.sndrcv("BlankingCheckIJKCell",*args)
  self.chk(rep)
  return rep.args[0].boolean
 def BlankingIsActive(self):
  rep=self.sndrcv("BlankingIsActive")
  self.chk(rep)
  return rep.args[0].boolean
 def BlankingIsNonDepthActive(self):
  rep=self.sndrcv("BlankingIsNonDepthActive")
  self.chk(rep)
  return rep.args[0].boolean
 def ColorMapCopyStandard(self,color_map):
  args=((ValueType.Scalar,c_int32,ContourColorMap(color_map).value),)
  rep=self.sndrcv("ColorMapCopyStandard",*args)
  self.chk(rep)
  return (rep.status == tecrpc.Reply.Success)
 def ColorMapCreateX(self,arg_list):
  args=((ValueType.Address,c_uint64,getattr(arg_list,'value',arg_list)),)
  rep=self.sndrcv("ColorMapCreateX",*args)
  self.chk(rep)
  return (rep.status == tecrpc.Reply.Success)
 def ColorMapDelete(self,source_color_map_name):
  args=((ValueType.Text,None,source_color_map_name),)
  rep=self.sndrcv("ColorMapDelete",*args)
  self.chk(rep)
 def ColorMapExists(self,color_map_name):
  args=((ValueType.Text,None,color_map_name),)
  rep=self.sndrcv("ColorMapExists",*args)
  self.chk(rep)
  return rep.args[0].boolean
 def ColorMapGetBasicColorRGB(self,basic_color):
  args=((ValueType.Scalar,c_int32,basic_color),)
  rep=self.sndrcv("ColorMapGetBasicColorRGB",*args)
  self.chk(rep)
  return (
   rep.args[0].uint32,
   rep.args[1].uint32,
   rep.args[2].uint32)
 def ColorMapGetContourRGB(self,color_map_number,contour_color_offset):
  args=((ValueType.Scalar,c_int32,color_map_number),
        (ValueType.Scalar,c_int32,contour_color_offset),)
  rep=self.sndrcv("ColorMapGetContourRGB",*args)
  self.chk(rep)
  return (
   rep.args[0].uint32,
   rep.args[1].uint32,
   rep.args[2].uint32)
 def ColorMapGetCount(self):
  rep=self.sndrcv("ColorMapGetCount")
  self.chk(rep)
  return rep.args[0].int32
 def ColorMapGetName(self,color_map_number):
  args=((ValueType.Scalar,c_int32,color_map_number),)
  rep=self.sndrcv("ColorMapGetName",*args)
  self.chk(rep)
  return self.read_text(rep.args[0])
 def ColorMapGetNumByName(self,color_map_name):
  args=((ValueType.Text,None,color_map_name),)
  rep=self.sndrcv("ColorMapGetNumByName",*args)
  self.chk(rep)
  return rep.args[0].int32
 def ColorMapIsBuiltIn(self,color_map_name):
  args=((ValueType.Text,None,color_map_name),)
  rep=self.sndrcv("ColorMapIsBuiltIn",*args)
  self.chk(rep)
  return rep.args[0].boolean
 def ColorMapNumBasicColors(self):
  rep=self.sndrcv("ColorMapNumBasicColors")
  self.chk(rep)
  return rep.args[0].int32
 def ColorMapRedistributeControlPts(self,color_map_name):
  args=((ValueType.Text,None,color_map_name),)
  rep=self.sndrcv("ColorMapRedistributeControlPts",*args)
  self.chk(rep)
  return (rep.status == tecrpc.Reply.Success)
 def ColorMapRefresh(self):
  rep=self.sndrcv("ColorMapRefresh")
  self.chk(rep)
 def ColorMapRename(self,source_color_map_name,new_color_map_name):
  args=((ValueType.Text,None,source_color_map_name),
        (ValueType.Text,None,new_color_map_name),)
  rep=self.sndrcv("ColorMapRename",*args)
  self.chk(rep)
 def ColorMapResetRawUserDefined(self,source_color_map_name):
  args=((ValueType.Text,None,source_color_map_name),)
  rep=self.sndrcv("ColorMapResetRawUserDefined",*args)
  self.chk(rep)
  return (rep.status == tecrpc.Reply.Success)
 def ColorMapSetBase(self,base_color_map):
  args=((ValueType.Scalar,c_int32,ContourColorMap(base_color_map).value),)
  rep=self.sndrcv("ColorMapSetBase",*args)
  self.chk(rep)
  return try_cast_to_enum(SetValueReturnCode, rep.args[0].int32)
 def ConnectGetPrevSharedZone(self,zones_to_consider,zone):
  args=((ValueType.Address,c_uint64,getattr(zones_to_consider,'value',zones_to_consider)),
        (ValueType.Scalar,c_int32,zone),)
  rep=self.sndrcv("ConnectGetPrevSharedZone",*args)
  self.chk(rep)
  return rep.args[0].int32
 def ConnectGetShareZoneSet(self,zone):
  args=((ValueType.Scalar,c_int32,zone),)
  rep=self.sndrcv("ConnectGetShareZoneSet",*args)
  self.chk(rep)
  return rep.args[0].uint64
 def ContourGetLevels(self,contour_group):
  args=((ValueType.Scalar,c_int32,contour_group),)
  rep=self.sndrcv("ContourGetLevels",*args)
  self.chk(rep)
  return (
   (rep.status == tecrpc.Reply.Success),
   len(rep.args[0].buffer)//sizeof(c_double),
   self.read_array(rep.args[0], c_double))
 def ContourLabelX(self,arg_list):
  args=((ValueType.Address,c_uint64,getattr(arg_list,'value',arg_list)),)
  rep=self.sndrcv("ContourLabelX",*args)
  self.chk(rep)
  return (rep.status == tecrpc.Reply.Success)
 def ContourLevelX(self,arg_list):
  args=((ValueType.Address,c_uint64,getattr(arg_list,'value',arg_list)),)
  rep=self.sndrcv("ContourLevelX",*args)
  self.chk(rep)
  return (rep.status == tecrpc.Reply.Success)
 def ContourSetVariable(self,new_variable):
  args=((ValueType.Scalar,c_int32,new_variable),)
  rep=self.sndrcv("ContourSetVariable",*args)
  self.chk(rep)
  return try_cast_to_enum(SetValueReturnCode, rep.args[0].int32)
 def ContourSetVariableX(self,arg_list):
  args=((ValueType.Address,c_uint64,getattr(arg_list,'value',arg_list)),)
  rep=self.sndrcv("ContourSetVariableX",*args)
  self.chk(rep)
  return try_cast_to_enum(SetValueReturnCode, rep.args[0].int32)
 def ConvAddPostReadCallback(self,converter_id_string,converter_post_read_callback):
  args=((ValueType.Text,None,converter_id_string),
        (ValueType.Address,c_uint64,getattr(converter_post_read_callback,'value',converter_post_read_callback)),)
  rep=self.sndrcv("ConvAddPostReadCallback",*args)
  self.chk(rep)
  return (rep.status == tecrpc.Reply.Success)
 def Convert3DPositionToGrid(self,x_position,y_position,z_position):
  args=((ValueType.Scalar,c_double,x_position),
        (ValueType.Scalar,c_double,y_position),
        (ValueType.Scalar,c_double,z_position),)
  rep=self.sndrcv("Convert3DPositionToGrid",*args)
  self.chk(rep)
  return (
   rep.args[0].float64,
   rep.args[1].float64,
   rep.args[2].float64)
 def ConvertGridTo3DPosition(self,x_grid_position,y_grid_position,z_grid_position):
  args=((ValueType.Scalar,c_double,x_grid_position),
        (ValueType.Scalar,c_double,y_grid_position),
        (ValueType.Scalar,c_double,z_grid_position),)
  rep=self.sndrcv("ConvertGridTo3DPosition",*args)
  self.chk(rep)
  return (
   rep.args[0].float64,
   rep.args[1].float64,
   rep.args[2].float64)
 def ConvertUnits(self,old_units,new_units,old_size):
  args=((ValueType.Scalar,c_int32,Units(old_units).value),
        (ValueType.Scalar,c_int32,Units(new_units).value),
        (ValueType.Scalar,c_double,old_size),)
  rep=self.sndrcv("ConvertUnits",*args)
  self.chk(rep)
  return rep.args[0].float64
 def ConvertXDimension(self,old_coord_sys,new_coord_sys,old_dimension):
  args=((ValueType.Scalar,c_int32,CoordSys(old_coord_sys).value),
        (ValueType.Scalar,c_int32,CoordSys(new_coord_sys).value),
        (ValueType.Scalar,c_double,old_dimension),)
  rep=self.sndrcv("ConvertXDimension",*args)
  self.chk(rep)
  return rep.args[0].float64
 def ConvertXPosition(self,old_coord_sys,new_coord_sys,old_x):
  args=((ValueType.Scalar,c_int32,CoordSys(old_coord_sys).value),
        (ValueType.Scalar,c_int32,CoordSys(new_coord_sys).value),
        (ValueType.Scalar,c_double,old_x),)
  rep=self.sndrcv("ConvertXPosition",*args)
  self.chk(rep)
  return rep.args[0].float64
 def ConvertYDimension(self,old_coord_sys,new_coord_sys,old_dimension):
  args=((ValueType.Scalar,c_int32,CoordSys(old_coord_sys).value),
        (ValueType.Scalar,c_int32,CoordSys(new_coord_sys).value),
        (ValueType.Scalar,c_double,old_dimension),)
  rep=self.sndrcv("ConvertYDimension",*args)
  self.chk(rep)
  return rep.args[0].float64
 def ConvertYPosition(self,old_coord_sys,new_coord_sys,old_y):
  args=((ValueType.Scalar,c_int32,CoordSys(old_coord_sys).value),
        (ValueType.Scalar,c_int32,CoordSys(new_coord_sys).value),
        (ValueType.Scalar,c_double,old_y),)
  rep=self.sndrcv("ConvertYPosition",*args)
  self.chk(rep)
  return rep.args[0].float64
 def CreateCircularZone(self,i_max,j_max,k_max,x_origin,y_origin,radius,z_min,z_max,field_data_type):
  args=((ValueType.Scalar,c_int64,i_max),
        (ValueType.Scalar,c_int64,j_max),
        (ValueType.Scalar,c_int64,k_max),
        (ValueType.Scalar,c_double,x_origin),
        (ValueType.Scalar,c_double,y_origin),
        (ValueType.Scalar,c_double,radius),
        (ValueType.Scalar,c_double,z_min),
        (ValueType.Scalar,c_double,z_max),
        (ValueType.Scalar,c_int32,FieldDataType(field_data_type).value),)
  rep=self.sndrcv("CreateCircularZone",*args)
  self.chk(rep)
  return (rep.status == tecrpc.Reply.Success)
 def CreateContourLineZones(self):
  rep=self.sndrcv("CreateContourLineZones")
  self.chk(rep)
  return (rep.status == tecrpc.Reply.Success)
 def CreateContourLineZonesX(self,arg_list):
  args=((ValueType.Address,c_uint64,getattr(arg_list,'value',arg_list)),)
  rep=self.sndrcv("CreateContourLineZonesX",*args)
  self.chk(rep)
  return (rep.status == tecrpc.Reply.Success)
 def CreateFEBoundary(self,source_zone,remove_blanked_surfaces):
  args=((ValueType.Scalar,c_int32,source_zone),
        (ValueType.Scalar,c_bool,remove_blanked_surfaces),)
  rep=self.sndrcv("CreateFEBoundary",*args)
  self.chk(rep)
  return (rep.status == tecrpc.Reply.Success)
 def CreateMirrorZones(self,source_zones,mirror_var):
  args=((ValueType.Address,c_uint64,getattr(source_zones,'value',source_zones)),
        (ValueType.Text,None,mirror_var),)
  rep=self.sndrcv("CreateMirrorZones",*args)
  self.chk(rep)
  return (rep.status == tecrpc.Reply.Success)
 def CreateRectangularZone(self,i_max,j_max,k_max,x_min,y_min,z_min,x_max,y_max,z_max,field_data_type):
  args=((ValueType.Scalar,c_int64,i_max),
        (ValueType.Scalar,c_int64,j_max),
        (ValueType.Scalar,c_int64,k_max),
        (ValueType.Scalar,c_double,x_min),
        (ValueType.Scalar,c_double,y_min),
        (ValueType.Scalar,c_double,z_min),
        (ValueType.Scalar,c_double,x_max),
        (ValueType.Scalar,c_double,y_max),
        (ValueType.Scalar,c_double,z_max),
        (ValueType.Scalar,c_int32,FieldDataType(field_data_type).value),)
  rep=self.sndrcv("CreateRectangularZone",*args)
  self.chk(rep)
  return (rep.status == tecrpc.Reply.Success)
 def CreateSimpleZone(self,num_points,v1_values,v2_values,field_data_type):
  args=((ValueType.Scalar,c_int64,num_points),
        (ValueType.Array,c_double,v1_values),
        (ValueType.Array,c_double,v2_values),
        (ValueType.Scalar,c_int32,FieldDataType(field_data_type).value),)
  rep=self.sndrcv("CreateSimpleZone",*args)
  self.chk(rep)
  return (rep.status == tecrpc.Reply.Success)
 def CreateSliceZoneFromPlane(self,slice_source,origin_x,origin_y,origin_z,normal_x,normal_y,normal_z):
  args=((ValueType.Scalar,c_int32,SliceSource(slice_source).value),
        (ValueType.Scalar,c_double,origin_x),
        (ValueType.Scalar,c_double,origin_y),
        (ValueType.Scalar,c_double,origin_z),
        (ValueType.Scalar,c_double,normal_x),
        (ValueType.Scalar,c_double,normal_y),
        (ValueType.Scalar,c_double,normal_z),)
  rep=self.sndrcv("CreateSliceZoneFromPlane",*args)
  self.chk(rep)
  return (rep.status == tecrpc.Reply.Success)
 def CreateSliceZoneFromPlneX(self,arg_list):
  args=((ValueType.Address,c_uint64,getattr(arg_list,'value',arg_list)),)
  rep=self.sndrcv("CreateSliceZoneFromPlneX",*args)
  self.chk(rep)
  return (rep.status == tecrpc.Reply.Success)
 def CreateSliceZoneShowTrace(self,do_show):
  args=((ValueType.Scalar,c_bool,do_show),)
  rep=self.sndrcv("CreateSliceZoneShowTrace",*args)
  self.chk(rep)
 def CreateSphericalZone(self,i_max,j_max,x_origin,y_origin,z_origin,radius,field_data_type):
  args=((ValueType.Scalar,c_int64,i_max),
        (ValueType.Scalar,c_int64,j_max),
        (ValueType.Scalar,c_double,x_origin),
        (ValueType.Scalar,c_double,y_origin),
        (ValueType.Scalar,c_double,z_origin),
        (ValueType.Scalar,c_double,radius),
        (ValueType.Scalar,c_int32,FieldDataType(field_data_type).value),)
  rep=self.sndrcv("CreateSphericalZone",*args)
  self.chk(rep)
  return (rep.status == tecrpc.Reply.Success)
 def CurveExtCrvFitAbbreviatedSettingsStringCallback(self,curve_fit_num):
  args=((ValueType.Scalar,c_int32,curve_fit_num),)
  rep=self.sndrcv("CurveExtCrvFitAbbreviatedSettingsStringCallback",*args)
  self.chk(rep)
  return rep.args[0].uint64
 def CurveExtCrvFitCount(self):
  rep=self.sndrcv("CurveExtCrvFitCount")
  self.chk(rep)
  return rep.args[0].int32
 def CurveExtCrvFitName(self,curve_fit_num):
  args=((ValueType.Scalar,c_int32,curve_fit_num),)
  rep=self.sndrcv("CurveExtCrvFitName",*args)
  self.chk(rep)
  return (
   (rep.status == tecrpc.Reply.Success),
   self.read_text(rep.args[0]))
 def CurveExtCrvFitSettingsCallback(self,curve_fit_num):
  args=((ValueType.Scalar,c_int32,curve_fit_num),)
  rep=self.sndrcv("CurveExtCrvFitSettingsCallback",*args)
  self.chk(rep)
  return rep.args[0].uint64
 def CurveGetDisplayInfo(self,line_map):
  args=((ValueType.Scalar,c_int32,line_map),)
  rep=self.sndrcv("CurveGetDisplayInfo",*args)
  self.chk(rep)
  return (
   (rep.status == tecrpc.Reply.Success),
   self.read_text(rep.args[0]))
 def CurveRegisterExtCrvFit(self,curve_fit_name,get_line_plot_data_points_callback,get_probe_value_callback,get_curve_info_string_callback,get_curve_settings_callback,get_abbreviated_settings_string_callback):
  args=((ValueType.Text,None,curve_fit_name),
        (ValueType.Address,c_uint64,getattr(get_line_plot_data_points_callback,'value',get_line_plot_data_points_callback)),
        (ValueType.Address,c_uint64,getattr(get_probe_value_callback,'value',get_probe_value_callback)),
        (ValueType.Address,c_uint64,getattr(get_curve_info_string_callback,'value',get_curve_info_string_callback)),
        (ValueType.Address,c_uint64,getattr(get_curve_settings_callback,'value',get_curve_settings_callback)),
        (ValueType.Address,c_uint64,getattr(get_abbreviated_settings_string_callback,'value',get_abbreviated_settings_string_callback)),)
  rep=self.sndrcv("CurveRegisterExtCrvFit",*args)
  self.chk(rep)
  return (rep.status == tecrpc.Reply.Success)
 def CurveSetExtendedSettings(self,line_map_num,settings):
  args=((ValueType.Scalar,c_int32,line_map_num),
        (ValueType.Text,None,settings),)
  rep=self.sndrcv("CurveSetExtendedSettings",*args)
  self.chk(rep)
  return try_cast_to_enum(SetValueReturnCode, rep.args[0].int32)
 def CurveWriteInfo(self,file_name,line_map,curve_info_mode):
  args=((ValueType.Text,None,file_name),
        (ValueType.Scalar,c_int32,line_map),
        (ValueType.Scalar,c_int32,CurveInfoMode(curve_info_mode).value),)
  rep=self.sndrcv("CurveWriteInfo",*args)
  self.chk(rep)
  return (rep.status == tecrpc.Reply.Success)
 def CustomLabelsAppend(self,label_list):
  args=((ValueType.Address,c_uint64,getattr(label_list,'value',label_list)),)
  rep=self.sndrcv("CustomLabelsAppend",*args)
  self.chk(rep)
  return (rep.status == tecrpc.Reply.Success)
 def CustomLabelsGet(self,which_set):
  args=((ValueType.Scalar,c_int32,which_set),)
  rep=self.sndrcv("CustomLabelsGet",*args)
  self.chk(rep)
  return (
   (rep.status == tecrpc.Reply.Success),
   rep.args[0].uint64)
 def CustomLabelsGetNumSets(self):
  rep=self.sndrcv("CustomLabelsGetNumSets")
  self.chk(rep)
  return rep.args[0].int32
 def DataAlter(self,equation,zone_set,i_min,i_max,i_skip,j_min,j_max,j_skip,k_min,k_max,k_skip,dest_data_type):
  args=((ValueType.Text,None,equation),
        (ValueType.Address,c_uint64,getattr(zone_set,'value',zone_set)),
        (ValueType.Scalar,c_int64,i_min),
        (ValueType.Scalar,c_int64,i_max),
        (ValueType.Scalar,c_int64,i_skip),
        (ValueType.Scalar,c_int64,j_min),
        (ValueType.Scalar,c_int64,j_max),
        (ValueType.Scalar,c_int64,j_skip),
        (ValueType.Scalar,c_int64,k_min),
        (ValueType.Scalar,c_int64,k_max),
        (ValueType.Scalar,c_int64,k_skip),
        (ValueType.Scalar,c_int32,FieldDataType(dest_data_type).value),)
  rep=self.sndrcv("DataAlter",*args)
  self.chk(rep)
  return (rep.status == tecrpc.Reply.Success)
 def DataAlterX(self,arg_list):
  args=((ValueType.Address,c_uint64,getattr(arg_list,'value',arg_list)),)
  rep=self.sndrcv("DataAlterX",*args)
  self.chk(rep)
  return (rep.status == tecrpc.Reply.Success)
 def DataAxialDuplicate(self,data_set_id,zones,spatial_vars,num_vectors,u_vars,v_vars,w_vars,is3_d_rotation,rotation_in_degrees,offset_angle_in_degrees,num_duplicates,origin,normal,add_zones_to_existing_strands):
  args=((ValueType.Scalar,c_int64,data_set_id),
        (ValueType.Address,c_uint64,getattr(zones,'value',zones)),
        (ValueType.Array,c_int32,spatial_vars),
        (ValueType.Scalar,c_int32,num_vectors),
        (ValueType.Array,c_int32,u_vars),
        (ValueType.Array,c_int32,v_vars),
        (ValueType.Array,c_int32,w_vars),
        (ValueType.Scalar,c_bool,is3_d_rotation),
        (ValueType.Scalar,c_double,rotation_in_degrees),
        (ValueType.Scalar,c_double,offset_angle_in_degrees),
        (ValueType.Scalar,c_int32,num_duplicates),
        (ValueType.Array,c_double,origin),
        (ValueType.Array,c_double,normal),
        (ValueType.Scalar,c_bool,add_zones_to_existing_strands),)
  rep=self.sndrcv("DataAxialDuplicate",*args)
  self.chk(rep)
  return (rep.status == tecrpc.Reply.Success)
 def DataConnectBranchShared(self,zone):
  args=((ValueType.Scalar,c_int32,zone),)
  rep=self.sndrcv("DataConnectBranchShared",*args)
  self.chk(rep)
  return (rep.status == tecrpc.Reply.Success)
 def DataConnectGetShareCount(self,zone):
  args=((ValueType.Scalar,c_int32,zone),)
  rep=self.sndrcv("DataConnectGetShareCount",*args)
  self.chk(rep)
  return rep.args[0].int32
 def DataConnectIsSZLData(self,zone):
  args=((ValueType.Scalar,c_int32,zone),)
  rep=self.sndrcv("DataConnectIsSZLData",*args)
  self.chk(rep)
  return rep.args[0].boolean
 def DataConnectIsSharingOk(self,source_zone,dest_zone):
  args=((ValueType.Scalar,c_int32,source_zone),
        (ValueType.Scalar,c_int32,dest_zone),)
  rep=self.sndrcv("DataConnectIsSharingOk",*args)
  self.chk(rep)
  return rep.args[0].boolean
 def DataConnectShare(self,source_zone,dest_zone):
  args=((ValueType.Scalar,c_int32,source_zone),
        (ValueType.Scalar,c_int32,dest_zone),)
  rep=self.sndrcv("DataConnectShare",*args)
  self.chk(rep)
 def DataElemGetFace(self,elem_to_face_map,elem,face_offset):
  args=((ValueType.Address,c_uint64,getattr(elem_to_face_map,'value',elem_to_face_map)),
        (ValueType.Scalar,c_int64,elem),
        (ValueType.Scalar,c_int32,face_offset),)
  rep=self.sndrcv("DataElemGetFace",*args)
  self.chk(rep)
  return rep.args[0].int64
 def DataElemGetNumFaces(self,elem_to_face_map,elem):
  args=((ValueType.Address,c_uint64,getattr(elem_to_face_map,'value',elem_to_face_map)),
        (ValueType.Scalar,c_int64,elem),)
  rep=self.sndrcv("DataElemGetNumFaces",*args)
  self.chk(rep)
  return rep.args[0].int32
 def DataElemGetReadableRef(self,zone):
  args=((ValueType.Scalar,c_int32,zone),)
  rep=self.sndrcv("DataElemGetReadableRef",*args)
  self.chk(rep)
  return rep.args[0].uint64
 def DataFECellGetNodes(self,zone,face,cell_index):
  args=((ValueType.Scalar,c_int32,zone),
        (ValueType.Scalar,c_int32,face),
        (ValueType.Scalar,c_int64,cell_index),)
  rep=self.sndrcv("DataFECellGetNodes",*args)
  self.chk(rep)
  return (
   rep.args[0].int64,
   rep.args[1].int64,
   rep.args[2].int64,
   rep.args[3].int64)
 def DataFECellGetUniqueNodes(self,zone,face_offset,cell_index,unique_nodes_size,unique_nodes):
  args=((ValueType.Scalar,c_int32,zone),
        (ValueType.Scalar,c_int32,face_offset),
        (ValueType.Scalar,c_int64,cell_index),
        (ValueType.Scalar,c_int32,unique_nodes_size),
        (ValueType.Array,c_int64,unique_nodes.contents),)
  rep=self.sndrcv("DataFECellGetUniqueNodes",*args)
  self.chk(rep)
  return (
   (rep.status == tecrpc.Reply.Success),
   len(rep.args[1].buffer)//sizeof(c_int64),
   rep.args[0].int32,
   self.read_array(rep.args[1], c_int64))
 def DataFaceMapAlloc(self,zone,num_faces,num_face_nodes,num_face_bndry_faces,num_face_bndry_conns):
  args=((ValueType.Scalar,c_int32,zone),
        (ValueType.Scalar,c_int64,num_faces),
        (ValueType.Scalar,c_int64,num_face_nodes),
        (ValueType.Scalar,c_int64,num_face_bndry_faces),
        (ValueType.Scalar,c_int64,num_face_bndry_conns),)
  rep=self.sndrcv("DataFaceMapAlloc",*args)
  self.chk(rep)
  return (rep.status == tecrpc.Reply.Success)
 def DataFaceMapAssignBConns(self,face_map,num_bndry_faces,num_bndry_conns_array,face_bndry_elems_array,face_bndry_elem_zones_array):
  args=((ValueType.Address,c_uint64,getattr(face_map,'value',face_map)),
        (ValueType.Scalar,c_int32,num_bndry_faces),
        (ValueType.Array,c_int32,num_bndry_conns_array),
        (ValueType.Array,c_int32,face_bndry_elems_array),
        (ValueType.Array,c_int32,face_bndry_elem_zones_array),)
  rep=self.sndrcv("DataFaceMapAssignBConns",*args)
  self.chk(rep)
 def DataFaceMapAssignBConns64(self,face_map,num_bndry_faces,num_bndry_conns_array,face_bndry_elems_array,face_bndry_elem_zones_array):
  args=((ValueType.Address,c_uint64,getattr(face_map,'value',face_map)),
        (ValueType.Scalar,c_int32,num_bndry_faces),
        (ValueType.Array,c_int32,num_bndry_conns_array),
        (ValueType.Array,c_int64,face_bndry_elems_array),
        (ValueType.Array,c_int32,face_bndry_elem_zones_array),)
  rep=self.sndrcv("DataFaceMapAssignBConns64",*args)
  self.chk(rep)
 def DataFaceMapAssignElemToNodeMap(self,face_map,num_elements,faces_per_elem_array,nodes_per_face_array,elem_to_node_map_array):
  args=((ValueType.Address,c_uint64,getattr(face_map,'value',face_map)),
        (ValueType.Scalar,c_int64,num_elements),
        (ValueType.Array,c_int32,faces_per_elem_array),
        (ValueType.Array,c_int32,nodes_per_face_array),
        (ValueType.Array,c_int32,elem_to_node_map_array),)
  rep=self.sndrcv("DataFaceMapAssignElemToNodeMap",*args)
  self.chk(rep)
  return (rep.status == tecrpc.Reply.Success)
 def DataFaceMapAssignElemToNodeMap64(self,face_map,num_elements,faces_per_elem_array,nodes_per_face_array,elem_to_node_map_array):
  args=((ValueType.Address,c_uint64,getattr(face_map,'value',face_map)),
        (ValueType.Scalar,c_int64,num_elements),
        (ValueType.Array,c_int32,faces_per_elem_array),
        (ValueType.Array,c_int32,nodes_per_face_array),
        (ValueType.Array,c_int64,elem_to_node_map_array),)
  rep=self.sndrcv("DataFaceMapAssignElemToNodeMap64",*args)
  self.chk(rep)
  return (rep.status == tecrpc.Reply.Success)
 def DataFaceMapAssignElems(self,face_map,num_faces,face_left_elems_array,face_right_elems_array):
  args=((ValueType.Address,c_uint64,getattr(face_map,'value',face_map)),
        (ValueType.Scalar,c_int64,num_faces),
        (ValueType.Array,c_int32,face_left_elems_array),
        (ValueType.Array,c_int32,face_right_elems_array),)
  rep=self.sndrcv("DataFaceMapAssignElems",*args)
  self.chk(rep)
 def DataFaceMapAssignElems64(self,face_map,num_faces,face_left_elems_array,face_right_elems_array):
  args=((ValueType.Address,c_uint64,getattr(face_map,'value',face_map)),
        (ValueType.Scalar,c_int64,num_faces),
        (ValueType.Array,c_int64,face_left_elems_array),
        (ValueType.Array,c_int64,face_right_elems_array),)
  rep=self.sndrcv("DataFaceMapAssignElems64",*args)
  self.chk(rep)
 def DataFaceMapAssignNodes(self,face_map,num_faces,num_face_nodes_array,face_nodes_array):
  args=((ValueType.Address,c_uint64,getattr(face_map,'value',face_map)),
        (ValueType.Scalar,c_int64,num_faces),
        (ValueType.Array,c_int32,num_face_nodes_array),
        (ValueType.Array,c_int32,face_nodes_array),)
  rep=self.sndrcv("DataFaceMapAssignNodes",*args)
  self.chk(rep)
 def DataFaceMapAssignNodes64(self,face_map,num_faces,num_face_nodes_array,face_nodes_array):
  args=((ValueType.Address,c_uint64,getattr(face_map,'value',face_map)),
        (ValueType.Scalar,c_int64,num_faces),
        (ValueType.Array,c_int32,num_face_nodes_array),
        (ValueType.Array,c_int64,face_nodes_array),)
  rep=self.sndrcv("DataFaceMapAssignNodes64",*args)
  self.chk(rep)
 def DataFaceMapBeginAssign(self,face_map):
  args=((ValueType.Address,c_uint64,getattr(face_map,'value',face_map)),)
  rep=self.sndrcv("DataFaceMapBeginAssign",*args)
  self.chk(rep)
 def DataFaceMapCustomLOD(self,zone,num_faces,num_face_nodes,num_face_bndry_faces,num_face_bndry_conns,load_callback,unload_callback,cleanup_callback,client_data):
  args=((ValueType.Scalar,c_int32,zone),
        (ValueType.Scalar,c_int64,num_faces),
        (ValueType.Scalar,c_int64,num_face_nodes),
        (ValueType.Scalar,c_int64,num_face_bndry_faces),
        (ValueType.Scalar,c_int64,num_face_bndry_conns),
        (ValueType.Address,c_uint64,getattr(load_callback,'value',load_callback)),
        (ValueType.Address,c_uint64,getattr(unload_callback,'value',unload_callback)),
        (ValueType.Address,c_uint64,getattr(cleanup_callback,'value',cleanup_callback)),
        (ValueType.ArbParam,None,client_data),)
  rep=self.sndrcv("DataFaceMapCustomLOD",*args)
  self.chk(rep)
  return (rep.status == tecrpc.Reply.Success)
 def DataFaceMapEndAssign(self,face_map):
  args=((ValueType.Address,c_uint64,getattr(face_map,'value',face_map)),)
  rep=self.sndrcv("DataFaceMapEndAssign",*args)
  self.chk(rep)
  return (rep.status == tecrpc.Reply.Success)
 def DataFaceMapGetBndryConn(self,face_map,face,bndry_conn_offset):
  args=((ValueType.Address,c_uint64,getattr(face_map,'value',face_map)),
        (ValueType.Scalar,c_int64,face),
        (ValueType.Scalar,c_int32,bndry_conn_offset),)
  rep=self.sndrcv("DataFaceMapGetBndryConn",*args)
  self.chk(rep)
  return (
   rep.args[0].int64,
   rep.args[1].int32)
 def DataFaceMapGetClientData(self,face_map):
  args=((ValueType.Address,c_uint64,getattr(face_map,'value',face_map)),)
  rep=self.sndrcv("DataFaceMapGetClientData",*args)
  self.chk(rep)
  return self.read_arbparam(rep.args[0])
 def DataFaceMapGetElementRawItemType(self,face_map):
  args=((ValueType.Address,c_uint64,getattr(face_map,'value',face_map)),)
  rep=self.sndrcv("DataFaceMapGetElementRawItemType",*args)
  self.chk(rep)
  return try_cast_to_enum(OffsetDataType, rep.args[0].int32)
 def DataFaceMapGetFaceNode(self,face_map,face,node_offset):
  args=((ValueType.Address,c_uint64,getattr(face_map,'value',face_map)),
        (ValueType.Scalar,c_int64,face),
        (ValueType.Scalar,c_int32,node_offset),)
  rep=self.sndrcv("DataFaceMapGetFaceNode",*args)
  self.chk(rep)
  return rep.args[0].int64
 def DataFaceMapGetLeftElem(self,face_map,face):
  args=((ValueType.Address,c_uint64,getattr(face_map,'value',face_map)),
        (ValueType.Scalar,c_int64,face),)
  rep=self.sndrcv("DataFaceMapGetLeftElem",*args)
  self.chk(rep)
  return rep.args[0].int64
 def DataFaceMapGetNBndryConns(self,face_map,face):
  args=((ValueType.Address,c_uint64,getattr(face_map,'value',face_map)),
        (ValueType.Scalar,c_int64,face),)
  rep=self.sndrcv("DataFaceMapGetNBndryConns",*args)
  self.chk(rep)
  return rep.args[0].int32
 def DataFaceMapGetNFaceNodes(self,face_map,face):
  args=((ValueType.Address,c_uint64,getattr(face_map,'value',face_map)),
        (ValueType.Scalar,c_int64,face),)
  rep=self.sndrcv("DataFaceMapGetNFaceNodes",*args)
  self.chk(rep)
  return rep.args[0].int32
 def DataFaceMapGetNFaces(self,face_map):
  args=((ValueType.Address,c_uint64,getattr(face_map,'value',face_map)),)
  rep=self.sndrcv("DataFaceMapGetNFaces",*args)
  self.chk(rep)
  return rep.args[0].int64
 def DataFaceMapGetNodeRawItemType(self,face_map):
  args=((ValueType.Address,c_uint64,getattr(face_map,'value',face_map)),)
  rep=self.sndrcv("DataFaceMapGetNodeRawItemType",*args)
  self.chk(rep)
  return try_cast_to_enum(OffsetDataType, rep.args[0].int32)
 def DataFaceMapGetNumNodes(self,face_map):
  args=((ValueType.Address,c_uint64,getattr(face_map,'value',face_map)),)
  rep=self.sndrcv("DataFaceMapGetNumNodes",*args)
  self.chk(rep)
  return rep.args[0].int64
 def DataFaceMapGetReadableRef(self,zone):
  args=((ValueType.Scalar,c_int32,zone),)
  rep=self.sndrcv("DataFaceMapGetReadableRef",*args)
  self.chk(rep)
  return rep.args[0].uint64
 def DataFaceMapGetRightElem(self,face_map,face):
  args=((ValueType.Address,c_uint64,getattr(face_map,'value',face_map)),
        (ValueType.Scalar,c_int64,face),)
  rep=self.sndrcv("DataFaceMapGetRightElem",*args)
  self.chk(rep)
  return rep.args[0].int64
 def DataFaceMapGetWritableRef(self,zone):
  args=((ValueType.Scalar,c_int32,zone),)
  rep=self.sndrcv("DataFaceMapGetWritableRef",*args)
  self.chk(rep)
  return rep.args[0].uint64
 def DataFaceMapSetDeferredMetadata(self,face_map,num_unique_faces,num_nodes_of_unique_faces,num_bndry_faces,num_bndry_conns):
  args=((ValueType.Address,c_uint64,getattr(face_map,'value',face_map)),
        (ValueType.Scalar,c_int64,num_unique_faces),
        (ValueType.Scalar,c_int64,num_nodes_of_unique_faces),
        (ValueType.Scalar,c_int64,num_bndry_faces),
        (ValueType.Scalar,c_int64,num_bndry_conns),)
  rep=self.sndrcv("DataFaceMapSetDeferredMetadata",*args)
  self.chk(rep)
  return (rep.status == tecrpc.Reply.Success)
 def DataFaceNbrAssignArrayByRef(self,face_neighbor,dest_offset,num_neighbors,neighbor_elems):
  args=((ValueType.Address,c_uint64,getattr(face_neighbor,'value',face_neighbor)),
        (ValueType.Scalar,c_int64,dest_offset),
        (ValueType.Scalar,c_int32,num_neighbors),
        (ValueType.Array,c_int32,neighbor_elems),)
  rep=self.sndrcv("DataFaceNbrAssignArrayByRef",*args)
  self.chk(rep)
 def DataFaceNbrAssignArrayByRef64(self,face_neighbor,dest_offset,num_neighbors,neighbor_elems):
  args=((ValueType.Address,c_uint64,getattr(face_neighbor,'value',face_neighbor)),
        (ValueType.Scalar,c_int64,dest_offset),
        (ValueType.Scalar,c_int32,num_neighbors),
        (ValueType.Array,c_int64,neighbor_elems),)
  rep=self.sndrcv("DataFaceNbrAssignArrayByRef64",*args)
  self.chk(rep)
 def DataFaceNbrAssignByRef(self,face_neighbor,element,face,nbrs_comp_obscure,num_neighbors,neighbor_elems,neighbor_zones):
  args=((ValueType.Address,c_uint64,getattr(face_neighbor,'value',face_neighbor)),
        (ValueType.Scalar,c_int64,element),
        (ValueType.Scalar,c_int32,face),
        (ValueType.Scalar,c_bool,nbrs_comp_obscure),
        (ValueType.Scalar,c_int32,num_neighbors),
        (ValueType.Array,c_int32,neighbor_elems),
        (ValueType.Array,c_int32,neighbor_zones),)
  rep=self.sndrcv("DataFaceNbrAssignByRef",*args)
  self.chk(rep)
  return (rep.status == tecrpc.Reply.Success)
 def DataFaceNbrAssignByRef64(self,face_neighbor,element,face,nbrs_comp_obscure,num_neighbors,neighbor_elems,neighbor_zones):
  args=((ValueType.Address,c_uint64,getattr(face_neighbor,'value',face_neighbor)),
        (ValueType.Scalar,c_int64,element),
        (ValueType.Scalar,c_int32,face),
        (ValueType.Scalar,c_bool,nbrs_comp_obscure),
        (ValueType.Scalar,c_int32,num_neighbors),
        (ValueType.Array,c_int64,neighbor_elems),
        (ValueType.Array,c_int32,neighbor_zones),)
  rep=self.sndrcv("DataFaceNbrAssignByRef64",*args)
  self.chk(rep)
  return (rep.status == tecrpc.Reply.Success)
 def DataFaceNbrBeginAssign(self,zone):
  args=((ValueType.Scalar,c_int32,zone),)
  rep=self.sndrcv("DataFaceNbrBeginAssign",*args)
  self.chk(rep)
  return (rep.status == tecrpc.Reply.Success)
 def DataFaceNbrCustomLOD(self,zone,auto_assign_fn,load_callback,unload_callback,cleanup_callback,client_data):
  args=((ValueType.Scalar,c_int32,zone),
        (ValueType.Scalar,c_bool,auto_assign_fn),
        (ValueType.Address,c_uint64,getattr(load_callback,'value',load_callback)),
        (ValueType.Address,c_uint64,getattr(unload_callback,'value',unload_callback)),
        (ValueType.Address,c_uint64,getattr(cleanup_callback,'value',cleanup_callback)),
        (ValueType.ArbParam,None,client_data),)
  rep=self.sndrcv("DataFaceNbrCustomLOD",*args)
  self.chk(rep)
  return (rep.status == tecrpc.Reply.Success)
 def DataFaceNbrEndAssign(self):
  rep=self.sndrcv("DataFaceNbrEndAssign")
  self.chk(rep)
  return (rep.status == tecrpc.Reply.Success)
 def DataFaceNbrFaceIsObscured(self,face_neighbor,element,face,active_zones):
  args=((ValueType.Address,c_uint64,getattr(face_neighbor,'value',face_neighbor)),
        (ValueType.Scalar,c_int64,element),
        (ValueType.Scalar,c_int32,face),
        (ValueType.Address,c_uint64,getattr(active_zones,'value',active_zones)),)
  rep=self.sndrcv("DataFaceNbrFaceIsObscured",*args)
  self.chk(rep)
  return rep.args[0].boolean
 def DataFaceNbrGetClientData(self,face_neighbor):
  args=((ValueType.Address,c_uint64,getattr(face_neighbor,'value',face_neighbor)),)
  rep=self.sndrcv("DataFaceNbrGetClientData",*args)
  self.chk(rep)
  return self.read_arbparam(rep.args[0])
 def DataFaceNbrGetModeByRef(self,face_neighbor):
  args=((ValueType.Address,c_uint64,getattr(face_neighbor,'value',face_neighbor)),)
  rep=self.sndrcv("DataFaceNbrGetModeByRef",*args)
  self.chk(rep)
  return try_cast_to_enum(FaceNeighborMode, rep.args[0].int32)
 def DataFaceNbrGetModeByZone(self,zone):
  args=((ValueType.Scalar,c_int32,zone),)
  rep=self.sndrcv("DataFaceNbrGetModeByZone",*args)
  self.chk(rep)
  return try_cast_to_enum(FaceNeighborMode, rep.args[0].int32)
 def DataFaceNbrGetNbrByRef(self,face_neighbor,element,face,neighbor_number):
  args=((ValueType.Address,c_uint64,getattr(face_neighbor,'value',face_neighbor)),
        (ValueType.Scalar,c_int64,element),
        (ValueType.Scalar,c_int32,face),
        (ValueType.Scalar,c_int32,neighbor_number),)
  rep=self.sndrcv("DataFaceNbrGetNbrByRef",*args)
  self.chk(rep)
  return (
   rep.args[0].int64,
   rep.args[1].int32)
 def DataFaceNbrGetNumNByRef(self,face_neighbor,element,face):
  args=((ValueType.Address,c_uint64,getattr(face_neighbor,'value',face_neighbor)),
        (ValueType.Scalar,c_int64,element),
        (ValueType.Scalar,c_int32,face),)
  rep=self.sndrcv("DataFaceNbrGetNumNByRef",*args)
  self.chk(rep)
  return (
   rep.args[0].int32,
   rep.args[1].boolean)
 def DataFaceNbrGetReadableRef(self,zone):
  args=((ValueType.Scalar,c_int32,zone),)
  rep=self.sndrcv("DataFaceNbrGetReadableRef",*args)
  self.chk(rep)
  return rep.args[0].uint64
 def DataFaceNbrRawItemType(self,face_neighbor):
  args=((ValueType.Address,c_uint64,getattr(face_neighbor,'value',face_neighbor)),)
  rep=self.sndrcv("DataFaceNbrRawItemType",*args)
  self.chk(rep)
  return try_cast_to_enum(OffsetDataType, rep.args[0].int32)
 def DataIJKCellGetIndices(self,zone,plane,cell_index):
  args=((ValueType.Scalar,c_int32,zone),
        (ValueType.Scalar,c_int32,IJKPlanes(plane).value),
        (ValueType.Scalar,c_int64,cell_index),)
  rep=self.sndrcv("DataIJKCellGetIndices",*args)
  self.chk(rep)
  return (
   rep.args[0].int64,
   rep.args[1].int64,
   rep.args[2].int64,
   rep.args[3].int64)
 def DataLoadBegin(self):
  rep=self.sndrcv("DataLoadBegin")
  self.chk(rep)
 def DataLoadEnd(self):
  rep=self.sndrcv("DataLoadEnd")
  self.chk(rep)
 def DataLoadFinishX(self,arg_list):
  args=((ValueType.Address,c_uint64,getattr(arg_list,'value',arg_list)),)
  rep=self.sndrcv("DataLoadFinishX",*args)
  self.chk(rep)
  return (
   (rep.status == tecrpc.Reply.Success),
   rep.args[0].int64)
 def DataLoadStart(self):
  rep=self.sndrcv("DataLoadStart")
  self.chk(rep)
 def DataNodeAlloc(self,zone):
  args=((ValueType.Scalar,c_int32,zone),)
  rep=self.sndrcv("DataNodeAlloc",*args)
  self.chk(rep)
  return (rep.status == tecrpc.Reply.Success)
 def DataNodeArrayGetByRef(self,source_node_map,source_offset,source_count,dest_node_array):
  args=((ValueType.Address,c_uint64,getattr(source_node_map,'value',source_node_map)),
        (ValueType.Scalar,c_int64,source_offset),
        (ValueType.Scalar,c_int64,source_count),
        (ValueType.Array,None,dest_node_array),)
  rep=self.sndrcv("DataNodeArrayGetByRef",*args)
  self.chk(rep)
  memmove(dest_node_array, rep.args[0].buffer, sizeof(dest_node_array))
 def DataNodeArraySetByRef(self,dest_node_map,dest_offset,dest_count,source_node_array):
  args=((ValueType.Address,c_uint64,getattr(dest_node_map,'value',dest_node_map)),
        (ValueType.Scalar,c_int64,dest_offset),
        (ValueType.Scalar,c_int64,dest_count),
        (ValueType.Array,c_int32,source_node_array),)
  rep=self.sndrcv("DataNodeArraySetByRef",*args)
  self.chk(rep)
 def DataNodeArraySetByRef64(self,dest_node_map,dest_offset,dest_count,source_node_array):
  args=((ValueType.Address,c_uint64,getattr(dest_node_map,'value',dest_node_map)),
        (ValueType.Scalar,c_int64,dest_offset),
        (ValueType.Scalar,c_int64,dest_count),
        (ValueType.Array,c_int64,source_node_array),)
  rep=self.sndrcv("DataNodeArraySetByRef64",*args)
  self.chk(rep)
 def DataNodeAutoLOD(self,zone,file_name,offset,is_data_native_byte_order):
  args=((ValueType.Scalar,c_int32,zone),
        (ValueType.Text,None,file_name),
        (ValueType.Scalar,c_int64,offset),
        (ValueType.Scalar,c_bool,is_data_native_byte_order),)
  rep=self.sndrcv("DataNodeAutoLOD",*args)
  self.chk(rep)
  return (rep.status == tecrpc.Reply.Success)
 def DataNodeCustomLOD(self,zone,load_callback,unload_callback,cleanup_callback,client_data):
  args=((ValueType.Scalar,c_int32,zone),
        (ValueType.Address,c_uint64,getattr(load_callback,'value',load_callback)),
        (ValueType.Address,c_uint64,getattr(unload_callback,'value',unload_callback)),
        (ValueType.Address,c_uint64,getattr(cleanup_callback,'value',cleanup_callback)),
        (ValueType.ArbParam,None,client_data),)
  rep=self.sndrcv("DataNodeCustomLOD",*args)
  self.chk(rep)
  return (rep.status == tecrpc.Reply.Success)
 def DataNodeCustomValueLOD(self,zone,load_callback,unload_callback,cleanup_callback,get_node_value,set_node_value,client_data):
  args=((ValueType.Scalar,c_int32,zone),
        (ValueType.Address,c_uint64,getattr(load_callback,'value',load_callback)),
        (ValueType.Address,c_uint64,getattr(unload_callback,'value',unload_callback)),
        (ValueType.Address,c_uint64,getattr(cleanup_callback,'value',cleanup_callback)),
        (ValueType.Address,c_uint64,getattr(get_node_value,'value',get_node_value)),
        (ValueType.Address,c_uint64,getattr(set_node_value,'value',set_node_value)),
        (ValueType.ArbParam,None,client_data),)
  rep=self.sndrcv("DataNodeCustomValueLOD",*args)
  self.chk(rep)
  return (rep.status == tecrpc.Reply.Success)
 def DataNodeGetByRef(self,node_map_ptr,element,corner):
  args=((ValueType.Address,c_uint64,getattr(node_map_ptr,'value',node_map_ptr)),
        (ValueType.Scalar,c_int64,element),
        (ValueType.Scalar,c_int32,corner),)
  rep=self.sndrcv("DataNodeGetByRef",*args)
  self.chk(rep)
  return rep.args[0].int64
 def DataNodeGetByZone(self,zone,element,corner):
  args=((ValueType.Scalar,c_int32,zone),
        (ValueType.Scalar,c_int64,element),
        (ValueType.Scalar,c_int32,corner),)
  rep=self.sndrcv("DataNodeGetByZone",*args)
  self.chk(rep)
  return rep.args[0].int64
 def DataNodeGetClientData(self,node_map):
  args=((ValueType.Address,c_uint64,getattr(node_map,'value',node_map)),)
  rep=self.sndrcv("DataNodeGetClientData",*args)
  self.chk(rep)
  return self.read_arbparam(rep.args[0])
 def DataNodeGetNodesPerElem(self,node_map_ptr):
  args=((ValueType.Address,c_uint64,getattr(node_map_ptr,'value',node_map_ptr)),)
  rep=self.sndrcv("DataNodeGetNodesPerElem",*args)
  self.chk(rep)
  return rep.args[0].int32
 def DataNodeGetRawItemType(self,node_map):
  args=((ValueType.Address,c_uint64,getattr(node_map,'value',node_map)),)
  rep=self.sndrcv("DataNodeGetRawItemType",*args)
  self.chk(rep)
  return try_cast_to_enum(OffsetDataType, rep.args[0].int32)
 def DataNodeGetRawPtrByRef(self,node_map):
  args=((ValueType.Address,c_uint64,getattr(node_map,'value',node_map)),)
  rep=self.sndrcv("DataNodeGetRawPtrByRef",*args)
  self.chk(rep)
 def DataNodeGetRawPtrByRef64(self,node_map):
  args=((ValueType.Address,c_uint64,getattr(node_map,'value',node_map)),)
  rep=self.sndrcv("DataNodeGetRawPtrByRef64",*args)
  self.chk(rep)
 def DataNodeGetReadableRef(self,zone):
  args=((ValueType.Scalar,c_int32,zone),)
  rep=self.sndrcv("DataNodeGetReadableRef",*args)
  self.chk(rep)
  return rep.args[0].uint64
 def DataNodeGetWritableRef(self,zone):
  args=((ValueType.Scalar,c_int32,zone),)
  rep=self.sndrcv("DataNodeGetWritableRef",*args)
  self.chk(rep)
  return rep.args[0].uint64
 def DataNodeRefGetGetFunc(self,node_map):
  args=((ValueType.Address,c_uint64,getattr(node_map,'value',node_map)),)
  rep=self.sndrcv("DataNodeRefGetGetFunc",*args)
  self.chk(rep)
  return rep.args[0].uint64
 def DataNodeRefGetSetFunc(self,node_map):
  args=((ValueType.Address,c_uint64,getattr(node_map,'value',node_map)),)
  rep=self.sndrcv("DataNodeRefGetSetFunc",*args)
  self.chk(rep)
  return rep.args[0].uint64
 def DataNodeSetByRef(self,nm,element,corner,node):
  args=((ValueType.Address,c_uint64,getattr(nm,'value',nm)),
        (ValueType.Scalar,c_int64,element),
        (ValueType.Scalar,c_int32,corner),
        (ValueType.Scalar,c_int64,node),)
  rep=self.sndrcv("DataNodeSetByRef",*args)
  self.chk(rep)
 def DataNodeSetByZone(self,zone,element,corner,node):
  args=((ValueType.Scalar,c_int32,zone),
        (ValueType.Scalar,c_int64,element),
        (ValueType.Scalar,c_int32,corner),
        (ValueType.Scalar,c_int64,node),)
  rep=self.sndrcv("DataNodeSetByZone",*args)
  self.chk(rep)
 def DataNodeToElemMapGetElem(self,node_to_elem_map,node,elem_offset):
  args=((ValueType.Address,c_uint64,getattr(node_to_elem_map,'value',node_to_elem_map)),
        (ValueType.Scalar,c_int64,node),
        (ValueType.Scalar,c_int64,elem_offset),)
  rep=self.sndrcv("DataNodeToElemMapGetElem",*args)
  self.chk(rep)
  return rep.args[0].int64
 def DataNodeToElemMapGetNumElems(self,node_to_elem_map,node):
  args=((ValueType.Address,c_uint64,getattr(node_to_elem_map,'value',node_to_elem_map)),
        (ValueType.Scalar,c_int64,node),)
  rep=self.sndrcv("DataNodeToElemMapGetNumElems",*args)
  self.chk(rep)
  return rep.args[0].int64
 def DataNodeToElemMapGetReadableRef(self,zone):
  args=((ValueType.Scalar,c_int32,zone),)
  rep=self.sndrcv("DataNodeToElemMapGetReadableRef",*args)
  self.chk(rep)
  return rep.args[0].uint64
 def DataRotate(self,data_set_id,zones,spatial_vars,num_vectors,u_vars,v_vars,w_vars,is3_d_rotation,rotation_in_degrees,origin,normal):
  args=((ValueType.Scalar,c_int64,data_set_id),
        (ValueType.Address,c_uint64,getattr(zones,'value',zones)),
        (ValueType.Array,c_int32,spatial_vars),
        (ValueType.Scalar,c_int32,num_vectors),
        (ValueType.Array,c_int32,u_vars),
        (ValueType.Array,c_int32,v_vars),
        (ValueType.Array,c_int32,w_vars),
        (ValueType.Scalar,c_bool,is3_d_rotation),
        (ValueType.Scalar,c_double,rotation_in_degrees),
        (ValueType.Array,c_double,origin),
        (ValueType.Array,c_double,normal),)
  rep=self.sndrcv("DataRotate",*args)
  self.chk(rep)
  return (rep.status == tecrpc.Reply.Success)
 def DataRotate2D(self,zone_set,rotate_amount_in_degrees,x_origin,y_origin):
  args=((ValueType.Address,c_uint64,getattr(zone_set,'value',zone_set)),
        (ValueType.Scalar,c_double,rotate_amount_in_degrees),
        (ValueType.Scalar,c_double,x_origin),
        (ValueType.Scalar,c_double,y_origin),)
  rep=self.sndrcv("DataRotate2D",*args)
  self.chk(rep)
  return (rep.status == tecrpc.Reply.Success)
 def DataSetAddJournalCommand(self,command_processor_id_string,instructions,raw_data):
  args=((ValueType.Text,None,command_processor_id_string),
        (ValueType.Text,None,instructions),
        (ValueType.Text,None,raw_data),)
  rep=self.sndrcv("DataSetAddJournalCommand",*args)
  self.chk(rep)
  return (rep.status == tecrpc.Reply.Success)
 def DataSetAddRawJournalCom(self,command):
  args=((ValueType.Text,None,command),)
  rep=self.sndrcv("DataSetAddRawJournalCom",*args)
  self.chk(rep)
  return (rep.status == tecrpc.Reply.Success)
 def DataSetAddTransientJournalCommand(self,command_processor_id_string,instructions,zones_created,raw_data):
  args=((ValueType.Text,None,command_processor_id_string),
        (ValueType.Text,None,instructions),
        (ValueType.Address,c_uint64,getattr(zones_created,'value',zones_created)),
        (ValueType.Text,None,raw_data),)
  rep=self.sndrcv("DataSetAddTransientJournalCommand",*args)
  self.chk(rep)
  return (rep.status == tecrpc.Reply.Success)
 def DataSetAddVar(self,var_name,field_data_type_array):
  args=((ValueType.Text,None,var_name),
        (ValueType.Array,c_int32,FieldDataType(field_data_type_array).value),)
  rep=self.sndrcv("DataSetAddVar",*args)
  self.chk(rep)
  return (rep.status == tecrpc.Reply.Success)
 def DataSetAddVarX(self,arg_list):
  args=((ValueType.Address,c_uint64,getattr(arg_list,'value',arg_list)),)
  rep=self.sndrcv("DataSetAddVarX",*args)
  self.chk(rep)
  return (rep.status == tecrpc.Reply.Success)
 def DataSetAddWriterX(self,arg_list):
  args=((ValueType.Address,c_uint64,getattr(arg_list,'value',arg_list)),)
  rep=self.sndrcv("DataSetAddWriterX",*args)
  self.chk(rep)
  return (rep.status == tecrpc.Reply.Success)
 def DataSetAddZone(self,name,i_max,j_max,k_max,zone_type,var_data_type_array):
  args=((ValueType.Text,None,name),
        (ValueType.Scalar,c_int64,i_max),
        (ValueType.Scalar,c_int64,j_max),
        (ValueType.Scalar,c_int64,k_max),
        (ValueType.Scalar,c_int32,ZoneType(zone_type).value),
        (ValueType.Array,c_int32,FieldDataType(var_data_type_array).value),)
  rep=self.sndrcv("DataSetAddZone",*args)
  self.chk(rep)
  return (rep.status == tecrpc.Reply.Success)
 def DataSetAddZoneX(self,arg_list):
  args=((ValueType.Address,c_uint64,getattr(arg_list,'value',arg_list)),)
  rep=self.sndrcv("DataSetAddZoneX",*args)
  self.chk(rep)
  return (rep.status == tecrpc.Reply.Success)
 def DataSetAttachOrphanedToFrameByOffset(self,orphaned_dataset_offset,frame_id):
  args=((ValueType.Scalar,c_int32,orphaned_dataset_offset),
        (ValueType.Scalar,c_int64,frame_id),)
  rep=self.sndrcv("DataSetAttachOrphanedToFrameByOffset",*args)
  self.chk(rep)
  return (rep.status == tecrpc.Reply.Success)
 def DataSetAttachOrphanedToFrameByUniqueID(self,orphaned_dataset_id,frame_id):
  args=((ValueType.Scalar,c_int64,orphaned_dataset_id),
        (ValueType.Scalar,c_int64,frame_id),)
  rep=self.sndrcv("DataSetAttachOrphanedToFrameByUniqueID",*args)
  self.chk(rep)
  return (rep.status == tecrpc.Reply.Success)
 def DataSetAutoAssignStrandIDs(self,zone_set):
  args=((ValueType.Address,c_uint64,getattr(zone_set,'value',zone_set)),)
  rep=self.sndrcv("DataSetAutoAssignStrandIDs",*args)
  self.chk(rep)
  return (rep.status == tecrpc.Reply.Success)
 def DataSetCreate(self,data_set_title,var_names,reset_style):
  args=((ValueType.Text,None,data_set_title),
        (ValueType.Address,c_uint64,getattr(var_names,'value',var_names)),
        (ValueType.Scalar,c_bool,reset_style),)
  rep=self.sndrcv("DataSetCreate",*args)
  self.chk(rep)
  return (rep.status == tecrpc.Reply.Success)
 def DataSetCreateX(self,arg_list):
  args=((ValueType.Address,c_uint64,getattr(arg_list,'value',arg_list)),)
  rep=self.sndrcv("DataSetCreateX",*args)
  self.chk(rep)
  return (rep.status == tecrpc.Reply.Success)
 def DataSetDeleteVar(self,var_list):
  args=((ValueType.Address,c_uint64,getattr(var_list,'value',var_list)),)
  rep=self.sndrcv("DataSetDeleteVar",*args)
  self.chk(rep)
  return (rep.status == tecrpc.Reply.Success)
 def DataSetDeleteZone(self,zone_list):
  args=((ValueType.Address,c_uint64,getattr(zone_list,'value',zone_list)),)
  rep=self.sndrcv("DataSetDeleteZone",*args)
  self.chk(rep)
  return (rep.status == tecrpc.Reply.Success)
 def DataSetGetActiveStrandIDs(self):
  rep=self.sndrcv("DataSetGetActiveStrandIDs")
  self.chk(rep)
  return rep.args[0].uint64
 def DataSetGetInfo(self):
  rep=self.sndrcv("DataSetGetInfo")
  self.chk(rep)
  return (
   (rep.status == tecrpc.Reply.Success),
   self.read_text(rep.args[0]),
   rep.args[1].int32,
   rep.args[2].int32)
 def DataSetGetInfoByUniqueID(self,data_set_id):
  args=((ValueType.Scalar,c_int64,data_set_id),)
  rep=self.sndrcv("DataSetGetInfoByUniqueID",*args)
  self.chk(rep)
  return (
   (rep.status == tecrpc.Reply.Success),
   self.read_text(rep.args[0]),
   rep.args[1].int32,
   rep.args[2].int32)
 def DataSetGetIntItemTypeForContentRange(self,max_value_stored_in_array):
  args=((ValueType.Scalar,c_int64,max_value_stored_in_array),)
  rep=self.sndrcv("DataSetGetIntItemTypeForContentRange",*args)
  self.chk(rep)
  return try_cast_to_enum(OffsetDataType, rep.args[0].int32)
 def DataSetGetMaxStrandID(self):
  rep=self.sndrcv("DataSetGetMaxStrandID")
  self.chk(rep)
  return rep.args[0].int32
 def DataSetGetNumVars(self):
  rep=self.sndrcv("DataSetGetNumVars")
  self.chk(rep)
  return rep.args[0].int32
 def DataSetGetNumVarsByUniqueID(self,data_set_id):
  args=((ValueType.Scalar,c_int64,data_set_id),)
  rep=self.sndrcv("DataSetGetNumVarsByUniqueID",*args)
  self.chk(rep)
  return rep.args[0].int32
 def DataSetGetNumVarsForFrame(self,frame_id):
  args=((ValueType.Scalar,c_int64,frame_id),)
  rep=self.sndrcv("DataSetGetNumVarsForFrame",*args)
  self.chk(rep)
  return rep.args[0].int32
 def DataSetGetNumZones(self):
  rep=self.sndrcv("DataSetGetNumZones")
  self.chk(rep)
  return rep.args[0].int32
 def DataSetGetNumZonesByUniqueID(self,data_set_id):
  args=((ValueType.Scalar,c_int64,data_set_id),)
  rep=self.sndrcv("DataSetGetNumZonesByUniqueID",*args)
  self.chk(rep)
  return rep.args[0].int32
 def DataSetGetNumZonesForFrame(self,frame_id):
  args=((ValueType.Scalar,c_int64,frame_id),)
  rep=self.sndrcv("DataSetGetNumZonesForFrame",*args)
  self.chk(rep)
  return rep.args[0].int32
 def DataSetGetRelevantZones(self,solution_time_min,solution_time_max,ignore_static_zones):
  args=((ValueType.Scalar,c_double,solution_time_min),
        (ValueType.Scalar,c_double,solution_time_max),
        (ValueType.Scalar,c_bool,ignore_static_zones),)
  rep=self.sndrcv("DataSetGetRelevantZones",*args)
  self.chk(rep)
  return rep.args[0].uint64
 def DataSetGetSZLRegistration(self):
  rep=self.sndrcv("DataSetGetSZLRegistration")
  self.chk(rep)
  return self.rep.args[0].uint64
 def DataSetGetStrandIDs(self):
  rep=self.sndrcv("DataSetGetStrandIDs")
  self.chk(rep)
  return rep.args[0].uint64
 def DataSetGetStrandRelevantZones(self,strand_id,solution_time_min,solution_time_max):
  args=((ValueType.Scalar,c_int32,strand_id),
        (ValueType.Scalar,c_double,solution_time_min),
        (ValueType.Scalar,c_double,solution_time_max),)
  rep=self.sndrcv("DataSetGetStrandRelevantZones",*args)
  self.chk(rep)
  return rep.args[0].uint64
 def DataSetGetUniqueID(self):
  rep=self.sndrcv("DataSetGetUniqueID")
  self.chk(rep)
  return rep.args[0].int64
 def DataSetGetVarLoadMode(self):
  rep=self.sndrcv("DataSetGetVarLoadMode")
  self.chk(rep)
  return try_cast_to_enum(VarLoadMode, rep.args[0].int32)
 def DataSetGetZonesForStrandID(self,strand_id):
  args=((ValueType.Scalar,c_int32,strand_id),)
  rep=self.sndrcv("DataSetGetZonesForStrandID",*args)
  self.chk(rep)
  return rep.args[0].uint64
 def DataSetIsAvailable(self):
  rep=self.sndrcv("DataSetIsAvailable")
  self.chk(rep)
  return rep.args[0].boolean
 def DataSetIsAvailableByUniqueID(self,unique_id):
  args=((ValueType.Scalar,c_int64,unique_id),)
  rep=self.sndrcv("DataSetIsAvailableByUniqueID",*args)
  self.chk(rep)
  return rep.args[0].boolean
 def DataSetIsAvailableForFrame(self,frame_id):
  args=((ValueType.Scalar,c_int64,frame_id),)
  rep=self.sndrcv("DataSetIsAvailableForFrame",*args)
  self.chk(rep)
  return rep.args[0].boolean
 def DataSetIsLODAllowed(self):
  rep=self.sndrcv("DataSetIsLODAllowed")
  self.chk(rep)
  return rep.args[0].boolean
 def DataSetIsLocked(self):
  rep=self.sndrcv("DataSetIsLocked")
  self.chk(rep)
  return (
   rep.args[0].boolean,
   self.read_text(rep.args[1]))
 def DataSetIsSharingAllowed(self):
  rep=self.sndrcv("DataSetIsSharingAllowed")
  self.chk(rep)
  return rep.args[0].boolean
 def DataSetIsUsedInLayout(self):
  rep=self.sndrcv("DataSetIsUsedInLayout")
  self.chk(rep)
  return rep.args[0].boolean
 def DataSetJournalIsValid(self):
  rep=self.sndrcv("DataSetJournalIsValid")
  self.chk(rep)
  return rep.args[0].boolean
 def DataSetLockOff(self,lock_string):
  args=((ValueType.Text,None,lock_string),)
  rep=self.sndrcv("DataSetLockOff",*args)
  self.chk(rep)
  return (rep.status == tecrpc.Reply.Success)
 def DataSetLockOn(self,lock_string):
  args=((ValueType.Text,None,lock_string),)
  rep=self.sndrcv("DataSetLockOn",*args)
  self.chk(rep)
  return (rep.status == tecrpc.Reply.Success)
 def DataSetMakeVarsAvailableByUniqueID(self,data_set_id,zones,vars_needed):
  args=((ValueType.Scalar,c_int64,data_set_id),
        (ValueType.Address,c_uint64,getattr(zones,'value',zones)),
        (ValueType.Address,c_uint64,getattr(vars_needed,'value',vars_needed)),)
  rep=self.sndrcv("DataSetMakeVarsAvailableByUniqueID",*args)
  self.chk(rep)
  return (rep.status == tecrpc.Reply.Success)
 def DataSetPostReadFinished(self,is_read_ok):
  args=((ValueType.Scalar,c_bool,is_read_ok),)
  rep=self.sndrcv("DataSetPostReadFinished",*args)
  self.chk(rep)
 def DataSetReadX(self,arg_list):
  args=((ValueType.Address,c_uint64,getattr(arg_list,'value',arg_list)),)
  rep=self.sndrcv("DataSetReadX",*args)
  self.chk(rep)
  return (rep.status == tecrpc.Reply.Success)
 def DataSetSetTitle(self,data_set_title):
  args=((ValueType.Text,None,data_set_title),)
  rep=self.sndrcv("DataSetSetTitle",*args)
  self.chk(rep)
  return (rep.status == tecrpc.Reply.Success)
 def DataSetSetTitleByUniqueID(self,unique_id,data_set_title):
  args=((ValueType.Scalar,c_int64,unique_id),
        (ValueType.Text,None,data_set_title),)
  rep=self.sndrcv("DataSetSetTitleByUniqueID",*args)
  self.chk(rep)
  return (rep.status == tecrpc.Reply.Success)
 def DataSetSuspendMarking(self,do_suspend):
  args=((ValueType.Scalar,c_bool,do_suspend),)
  rep=self.sndrcv("DataSetSuspendMarking",*args)
  self.chk(rep)
 def DataSetWriteX(self,arg_list):
  args=((ValueType.Address,c_uint64,getattr(arg_list,'value',arg_list)),)
  rep=self.sndrcv("DataSetWriteX",*args)
  self.chk(rep)
  return (rep.status == tecrpc.Reply.Success)
 def DataValueAlloc(self,zone,var):
  args=((ValueType.Scalar,c_int32,zone),
        (ValueType.Scalar,c_int32,var),)
  rep=self.sndrcv("DataValueAlloc",*args)
  self.chk(rep)
  return (rep.status == tecrpc.Reply.Success)
 def DataValueArrayGetByRef(self,source_field_data,source_offset,source_count,dest_value_array):
  args=((ValueType.Address,c_uint64,getattr(source_field_data,'value',source_field_data)),
        (ValueType.Scalar,c_int64,source_offset),
        (ValueType.Scalar,c_int64,source_count),
        (ValueType.Array,None,dest_value_array),)
  rep=self.sndrcv("DataValueArrayGetByRef",*args)
  self.chk(rep)
  memmove(dest_value_array, rep.args[0].buffer, sizeof(dest_value_array))
 def DataValueArraySetByRef(self,dest_field_data,dest_offset,dest_count,source_value_array):
  args=((ValueType.Address,c_uint64,getattr(dest_field_data,'value',dest_field_data)),
        (ValueType.Scalar,c_int64,dest_offset),
        (ValueType.Scalar,c_int64,dest_count),
        (ValueType.Array,c_uint8,source_value_array),)
  rep=self.sndrcv("DataValueArraySetByRef",*args)
  self.chk(rep)
 def DataValueAutoLOD(self,zone,var,data_value_structure,file_name,offset,stride,is_data_native_byte_order):
  args=((ValueType.Scalar,c_int32,zone),
        (ValueType.Scalar,c_int32,var),
        (ValueType.Scalar,c_int32,DataValueStructure(data_value_structure).value),
        (ValueType.Text,None,file_name),
        (ValueType.Scalar,c_int64,offset),
        (ValueType.Scalar,c_int64,stride),
        (ValueType.Scalar,c_bool,is_data_native_byte_order),)
  rep=self.sndrcv("DataValueAutoLOD",*args)
  self.chk(rep)
  return (rep.status == tecrpc.Reply.Success)
 def DataValueBranchShared(self,zone,var,copy_shared_data):
  args=((ValueType.Scalar,c_int32,zone),
        (ValueType.Scalar,c_int32,var),
        (ValueType.Scalar,c_bool,copy_shared_data),)
  rep=self.sndrcv("DataValueBranchShared",*args)
  self.chk(rep)
  return (rep.status == tecrpc.Reply.Success)
 def DataValueCopy(self,source_zone,dest_zone,var):
  args=((ValueType.Scalar,c_int32,source_zone),
        (ValueType.Scalar,c_int32,dest_zone),
        (ValueType.Scalar,c_int32,var),)
  rep=self.sndrcv("DataValueCopy",*args)
  self.chk(rep)
  return (rep.status == tecrpc.Reply.Success)
 def DataValueCustomLOD(self,zone,var,variable_load,variable_unload,variable_cleanup,get_value_function,set_value_function,client_data):
  args=((ValueType.Scalar,c_int32,zone),
        (ValueType.Scalar,c_int32,var),
        (ValueType.Address,c_uint64,getattr(variable_load,'value',variable_load)),
        (ValueType.Address,c_uint64,getattr(variable_unload,'value',variable_unload)),
        (ValueType.Address,c_uint64,getattr(variable_cleanup,'value',variable_cleanup)),
        (ValueType.Address,c_uint64,getattr(get_value_function,'value',get_value_function)),
        (ValueType.Address,c_uint64,getattr(set_value_function,'value',set_value_function)),
        (ValueType.ArbParam,None,client_data),)
  rep=self.sndrcv("DataValueCustomLOD",*args)
  self.chk(rep)
  return (rep.status == tecrpc.Reply.Success)
 def DataValueGetByRef(self,field_data,point_index):
  args=((ValueType.Address,c_uint64,getattr(field_data,'value',field_data)),
        (ValueType.Scalar,c_int64,point_index),)
  rep=self.sndrcv("DataValueGetByRef",*args)
  self.chk(rep)
  return rep.args[0].float64
 def DataValueGetByZoneVar(self,zone,var,value_index):
  args=((ValueType.Scalar,c_int32,zone),
        (ValueType.Scalar,c_int32,var),
        (ValueType.Scalar,c_int64,value_index),)
  rep=self.sndrcv("DataValueGetByZoneVar",*args)
  self.chk(rep)
  return rep.args[0].float64
 def DataValueGetClientData(self,field_data):
  args=((ValueType.Address,c_uint64,getattr(field_data,'value',field_data)),)
  rep=self.sndrcv("DataValueGetClientData",*args)
  self.chk(rep)
  return self.read_arbparam(rep.args[0])
 def DataValueGetCountByRef(self,field_data):
  args=((ValueType.Address,c_uint64,getattr(field_data,'value',field_data)),)
  rep=self.sndrcv("DataValueGetCountByRef",*args)
  self.chk(rep)
  return rep.args[0].int64
 def DataValueGetLocation(self,zone,var):
  args=((ValueType.Scalar,c_int32,zone),
        (ValueType.Scalar,c_int32,var),)
  rep=self.sndrcv("DataValueGetLocation",*args)
  self.chk(rep)
  return try_cast_to_enum(ValueLocation, rep.args[0].int32)
 def DataValueGetLocationByRef(self,field_data):
  args=((ValueType.Address,c_uint64,getattr(field_data,'value',field_data)),)
  rep=self.sndrcv("DataValueGetLocationByRef",*args)
  self.chk(rep)
  return try_cast_to_enum(ValueLocation, rep.args[0].int32)
 def DataValueGetMinMaxByRef(self,field_data):
  args=((ValueType.Address,c_uint64,getattr(field_data,'value',field_data)),)
  rep=self.sndrcv("DataValueGetMinMaxByRef",*args)
  self.chk(rep)
  return (
   rep.args[0].float64,
   rep.args[1].float64)
 def DataValueGetMinMaxByZoneVar(self,zone,var):
  args=((ValueType.Scalar,c_int32,zone),
        (ValueType.Scalar,c_int32,var),)
  rep=self.sndrcv("DataValueGetMinMaxByZoneVar",*args)
  self.chk(rep)
  return (
   (rep.status == tecrpc.Reply.Success),
   rep.args[0].float64,
   rep.args[1].float64)
 def DataValueGetPrevSharedZone(self,zones_to_consider,zone,var):
  args=((ValueType.Address,c_uint64,getattr(zones_to_consider,'value',zones_to_consider)),
        (ValueType.Scalar,c_int32,zone),
        (ValueType.Scalar,c_int32,var),)
  rep=self.sndrcv("DataValueGetPrevSharedZone",*args)
  self.chk(rep)
  return rep.args[0].int32
 def DataValueGetRawPtrByRef(self,field_data):
  args=((ValueType.Address,c_uint64,getattr(field_data,'value',field_data)),)
  rep=self.sndrcv("DataValueGetRawPtrByRef",*args)
  self.chk(rep)
  return self.rep.args[0].uint64
 def DataValueGetReadableCCRef(self,zone,var):
  args=((ValueType.Scalar,c_int32,zone),
        (ValueType.Scalar,c_int32,var),)
  rep=self.sndrcv("DataValueGetReadableCCRef",*args)
  self.chk(rep)
  return rep.args[0].uint64
 def DataValueGetReadableDerivedRef(self,zone,var):
  args=((ValueType.Scalar,c_int32,zone),
        (ValueType.Scalar,c_int32,var),)
  rep=self.sndrcv("DataValueGetReadableDerivedRef",*args)
  self.chk(rep)
  return rep.args[0].uint64
 def DataValueGetReadableNLRef(self,zone,var):
  args=((ValueType.Scalar,c_int32,zone),
        (ValueType.Scalar,c_int32,var),)
  rep=self.sndrcv("DataValueGetReadableNLRef",*args)
  self.chk(rep)
  return rep.args[0].uint64
 def DataValueGetReadableNativeRef(self,zone,var):
  args=((ValueType.Scalar,c_int32,zone),
        (ValueType.Scalar,c_int32,var),)
  rep=self.sndrcv("DataValueGetReadableNativeRef",*args)
  self.chk(rep)
  return rep.args[0].uint64
 def DataValueGetReadableNativeRefByUniqueID(self,dataset_id,zone,var):
  args=((ValueType.Scalar,c_int64,dataset_id),
        (ValueType.Scalar,c_int32,zone),
        (ValueType.Scalar,c_int32,var),)
  rep=self.sndrcv("DataValueGetReadableNativeRefByUniqueID",*args)
  self.chk(rep)
  return rep.args[0].uint64
 def DataValueGetRefType(self,field_data):
  args=((ValueType.Address,c_uint64,getattr(field_data,'value',field_data)),)
  rep=self.sndrcv("DataValueGetRefType",*args)
  self.chk(rep)
  return try_cast_to_enum(FieldDataType, rep.args[0].int32)
 def DataValueGetShareCount(self,zone,var):
  args=((ValueType.Scalar,c_int32,zone),
        (ValueType.Scalar,c_int32,var),)
  rep=self.sndrcv("DataValueGetShareCount",*args)
  self.chk(rep)
  return rep.args[0].int32
 def DataValueGetShareZoneSet(self,zone,var):
  args=((ValueType.Scalar,c_int32,zone),
        (ValueType.Scalar,c_int32,var),)
  rep=self.sndrcv("DataValueGetShareZoneSet",*args)
  self.chk(rep)
  return rep.args[0].uint64
 def DataValueGetType(self,zone,var):
  args=((ValueType.Scalar,c_int32,zone),
        (ValueType.Scalar,c_int32,var),)
  rep=self.sndrcv("DataValueGetType",*args)
  self.chk(rep)
  return try_cast_to_enum(FieldDataType, rep.args[0].int32)
 def DataValueGetWritableNativeRef(self,zone,var):
  args=((ValueType.Scalar,c_int32,zone),
        (ValueType.Scalar,c_int32,var),)
  rep=self.sndrcv("DataValueGetWritableNativeRef",*args)
  self.chk(rep)
  return rep.args[0].uint64
 def DataValueGetWritableNativeRefByUniqueID(self,dataset_id,zone,var):
  args=((ValueType.Scalar,c_int64,dataset_id),
        (ValueType.Scalar,c_int32,zone),
        (ValueType.Scalar,c_int32,var),)
  rep=self.sndrcv("DataValueGetWritableNativeRefByUniqueID",*args)
  self.chk(rep)
  return rep.args[0].uint64
 def DataValueGetZoneVarByRef(self,fd):
  args=((ValueType.Address,c_uint64,getattr(fd,'value',fd)),)
  rep=self.sndrcv("DataValueGetZoneVarByRef",*args)
  self.chk(rep)
  return (
   (rep.status == tecrpc.Reply.Success),
   rep.args[0].int32,
   rep.args[1].int32)
 def DataValueIsLoaded(self,zone,var):
  args=((ValueType.Scalar,c_int32,zone),
        (ValueType.Scalar,c_int32,var),)
  rep=self.sndrcv("DataValueIsLoaded",*args)
  self.chk(rep)
  return rep.args[0].boolean
 def DataValueIsMinMaxValidByZoneVar(self,zone,var):
  args=((ValueType.Scalar,c_int32,zone),
        (ValueType.Scalar,c_int32,var),)
  rep=self.sndrcv("DataValueIsMinMaxValidByZoneVar",*args)
  self.chk(rep)
  return rep.args[0].boolean
 def DataValueIsPassive(self,zone,var):
  args=((ValueType.Scalar,c_int32,zone),
        (ValueType.Scalar,c_int32,var),)
  rep=self.sndrcv("DataValueIsPassive",*args)
  self.chk(rep)
  return rep.args[0].boolean
 def DataValueIsSharingOk(self,source_zone,dest_zone,var):
  args=((ValueType.Scalar,c_int32,source_zone),
        (ValueType.Scalar,c_int32,dest_zone),
        (ValueType.Scalar,c_int32,var),)
  rep=self.sndrcv("DataValueIsSharingOk",*args)
  self.chk(rep)
  return rep.args[0].boolean
 def DataValueRefGetGetFunc(self,fd):
  args=((ValueType.Address,c_uint64,getattr(fd,'value',fd)),)
  rep=self.sndrcv("DataValueRefGetGetFunc",*args)
  self.chk(rep)
  return rep.args[0].uint64
 def DataValueRefGetSetFunc(self,fd):
  args=((ValueType.Address,c_uint64,getattr(fd,'value',fd)),)
  rep=self.sndrcv("DataValueRefGetSetFunc",*args)
  self.chk(rep)
  return rep.args[0].uint64
 def DataValueSetByRef(self,fd,point_index,value):
  args=((ValueType.Address,c_uint64,getattr(fd,'value',fd)),
        (ValueType.Scalar,c_int64,point_index),
        (ValueType.Scalar,c_double,value),)
  rep=self.sndrcv("DataValueSetByRef",*args)
  self.chk(rep)
 def DataValueSetByZoneVar(self,zone,var,point_index,value):
  args=((ValueType.Scalar,c_int32,zone),
        (ValueType.Scalar,c_int32,var),
        (ValueType.Scalar,c_int64,point_index),
        (ValueType.Scalar,c_double,value),)
  rep=self.sndrcv("DataValueSetByZoneVar",*args)
  self.chk(rep)
  return (rep.status == tecrpc.Reply.Success)
 def DataValueSetByZoneVarX(self,arg_list):
  args=((ValueType.Address,c_uint64,getattr(arg_list,'value',arg_list)),)
  rep=self.sndrcv("DataValueSetByZoneVarX",*args)
  self.chk(rep)
  return (rep.status == tecrpc.Reply.Success)
 def DataValueSetMinMaxByRef(self,field_data,min_value,max_value):
  args=((ValueType.Address,c_uint64,getattr(field_data,'value',field_data)),
        (ValueType.Scalar,c_double,min_value),
        (ValueType.Scalar,c_double,max_value),)
  rep=self.sndrcv("DataValueSetMinMaxByRef",*args)
  self.chk(rep)
 def DataValueSetMinMaxByZoneVar(self,zone,var,min_value,max_value):
  args=((ValueType.Scalar,c_int32,zone),
        (ValueType.Scalar,c_int32,var),
        (ValueType.Scalar,c_double,min_value),
        (ValueType.Scalar,c_double,max_value),)
  rep=self.sndrcv("DataValueSetMinMaxByZoneVar",*args)
  self.chk(rep)
 def DataValueShare(self,source_zone,dest_zone,var):
  args=((ValueType.Scalar,c_int32,source_zone),
        (ValueType.Scalar,c_int32,dest_zone),
        (ValueType.Scalar,c_int32,var),)
  rep=self.sndrcv("DataValueShare",*args)
  self.chk(rep)
 def DataValueUnload(self,zone,var):
  args=((ValueType.Scalar,c_int32,zone),
        (ValueType.Scalar,c_int32,var),)
  rep=self.sndrcv("DataValueUnload",*args)
  self.chk(rep)
  return (rep.status == tecrpc.Reply.Success)
 def Delay(self,seconds):
  args=((ValueType.Scalar,c_int32,seconds),)
  rep=self.sndrcv("Delay",*args)
  self.chk(rep)
  return (rep.status == tecrpc.Reply.Success)
 def DialogAllowDoubleClickLaunch(self,dialog,do_allow):
  args=((ValueType.Scalar,c_int32,Dialog(dialog).value),
        (ValueType.Scalar,c_bool,do_allow),)
  rep=self.sndrcv("DialogAllowDoubleClickLaunch",*args)
  self.chk(rep)
 def DialogCheckPercentDone(self,percent_done):
  args=((ValueType.Scalar,c_int32,percent_done),)
  rep=self.sndrcv("DialogCheckPercentDone",*args)
  self.chk(rep)
  return (rep.status == tecrpc.Reply.Success)
 def DialogDrop(self,dialog_to_drop):
  args=((ValueType.Scalar,c_int32,Dialog(dialog_to_drop).value),)
  rep=self.sndrcv("DialogDrop",*args)
  self.chk(rep)
  return (rep.status == tecrpc.Reply.Success)
 def DialogDropPercentDone(self):
  rep=self.sndrcv("DialogDropPercentDone")
  self.chk(rep)
 def DialogErrMsg(self,message):
  args=((ValueType.Text,None,message),)
  rep=self.sndrcv("DialogErrMsg",*args)
  self.chk(rep)
 def DialogGetSimpleText(self,instructions,default_text):
  args=((ValueType.Text,None,instructions),
        (ValueType.Text,None,default_text),)
  rep=self.sndrcv("DialogGetSimpleText",*args)
  self.chk(rep)
  return (
   (rep.status == tecrpc.Reply.Success),
   self.read_text(rep.args[0]))
 def DialogLastMessageBox(self):
  rep=self.sndrcv("DialogLastMessageBox")
  self.chk(rep)
  return (rep.status == tecrpc.Reply.Success)
 def DialogLaunch(self,dialog_to_launch):
  args=((ValueType.Scalar,c_int32,Dialog(dialog_to_launch).value),)
  rep=self.sndrcv("DialogLaunch",*args)
  self.chk(rep)
  return (rep.status == tecrpc.Reply.Success)
 def DialogLaunchPercentDone(self,label,show_the_scale):
  args=((ValueType.Text,None,label),
        (ValueType.Scalar,c_bool,show_the_scale),)
  rep=self.sndrcv("DialogLaunchPercentDone",*args)
  self.chk(rep)
 def DialogMessageBox(self,message,message_box_type):
  args=((ValueType.Text,None,message),
        (ValueType.Scalar,c_int32,MessageBoxType(message_box_type).value),)
  rep=self.sndrcv("DialogMessageBox",*args)
  self.chk(rep)
  return (rep.status == tecrpc.Reply.Success)
 def DialogSetPercentDoneText(self,text):
  args=((ValueType.Text,None,text),)
  rep=self.sndrcv("DialogSetPercentDoneText",*args)
  self.chk(rep)
 def DispatchWorkAreaEvent(self,i,j,button_or_key,event,is_shifted,is_alted,is_controlled):
  args=((ValueType.Scalar,c_int32,i),
        (ValueType.Scalar,c_int32,j),
        (ValueType.Scalar,c_int32,button_or_key),
        (ValueType.Scalar,c_int32,Event(event).value),
        (ValueType.Scalar,c_bool,is_shifted),
        (ValueType.Scalar,c_bool,is_alted),
        (ValueType.Scalar,c_bool,is_controlled),)
  rep=self.sndrcv("DispatchWorkAreaEvent",*args)
  self.chk(rep)
 def DrawGraphics(self,do_drawing):
  args=((ValueType.Scalar,c_bool,do_drawing),)
  rep=self.sndrcv("DrawGraphics",*args)
  self.chk(rep)
  return (rep.status == tecrpc.Reply.Success)
 def DropOpeningBanner(self):
  rep=self.sndrcv("DropOpeningBanner")
  self.chk(rep)
 def DynamicLabelRegisterCallback(self,dynamic_label_name,dynamic_label_callback,client_data):
  args=((ValueType.Text,None,dynamic_label_name),
        (ValueType.Address,c_uint64,getattr(dynamic_label_callback,'value',dynamic_label_callback)),
        (ValueType.ArbParam,None,client_data),)
  rep=self.sndrcv("DynamicLabelRegisterCallback",*args)
  self.chk(rep)
 def ElapseTimeInMS(self):
  rep=self.sndrcv("ElapseTimeInMS")
  self.chk(rep)
  return rep.args[0].int64
 def ElemOrientGetOrientation(self,element_orientation,element):
  args=((ValueType.Address,c_uint64,getattr(element_orientation,'value',element_orientation)),
        (ValueType.Scalar,c_int64,element),)
  rep=self.sndrcv("ElemOrientGetOrientation",*args)
  self.chk(rep)
  return try_cast_to_enum(ElementOrientation, rep.args[0].int32)
 def ElemOrientGetReadableRef(self,zone):
  args=((ValueType.Scalar,c_int32,zone),)
  rep=self.sndrcv("ElemOrientGetReadableRef",*args)
  self.chk(rep)
  return rep.args[0].uint64
 def EventAddPostDrawCallback(self,draw_event_callback,client_data):
  args=((ValueType.Address,c_uint64,getattr(draw_event_callback,'value',draw_event_callback)),
        (ValueType.ArbParam,None,client_data),)
  rep=self.sndrcv("EventAddPostDrawCallback",*args)
  self.chk(rep)
  return (rep.status == tecrpc.Reply.Success)
 def EventAddPreDrawCallback(self,draw_event_callback,client_data):
  args=((ValueType.Address,c_uint64,getattr(draw_event_callback,'value',draw_event_callback)),
        (ValueType.ArbParam,None,client_data),)
  rep=self.sndrcv("EventAddPreDrawCallback",*args)
  self.chk(rep)
  return (rep.status == tecrpc.Reply.Success)
 def Export(self,append):
  args=((ValueType.Scalar,c_bool,append),)
  rep=self.sndrcv("Export",*args)
  self.chk(rep)
  return (rep.status == tecrpc.Reply.Success)
 def ExportCancel(self):
  rep=self.sndrcv("ExportCancel")
  self.chk(rep)
 def ExportFinish(self):
  rep=self.sndrcv("ExportFinish")
  self.chk(rep)
  return rep.args[0].boolean
 def ExportIsRecording(self):
  rep=self.sndrcv("ExportIsRecording")
  self.chk(rep)
  return rep.args[0].boolean
 def ExportNextFrame(self):
  rep=self.sndrcv("ExportNextFrame")
  self.chk(rep)
  return (rep.status == tecrpc.Reply.Success)
 def ExportSetup(self,attribute,sub_attribute,d_value,i_value):
  args=((ValueType.Text,None,attribute),
        (ValueType.Text,None,sub_attribute),
        (ValueType.Scalar,c_double,d_value),
        (ValueType.ArbParam,None,i_value),)
  rep=self.sndrcv("ExportSetup",*args)
  self.chk(rep)
  return try_cast_to_enum(SetValueReturnCode, rep.args[0].int32)
 def ExportStart(self):
  rep=self.sndrcv("ExportStart")
  self.chk(rep)
  return (rep.status == tecrpc.Reply.Success)
 def ExtendedScatterSymbolGetManager(self):
  rep=self.sndrcv("ExtendedScatterSymbolGetManager")
  self.chk(rep)
  return self.rep.args[0].uint64
 def ExtractConnectedRegionsX(self,arg_list):
  args=((ValueType.Address,c_uint64,getattr(arg_list,'value',arg_list)),)
  rep=self.sndrcv("ExtractConnectedRegionsX",*args)
  self.chk(rep)
  return (rep.status == tecrpc.Reply.Success)
 def ExtractFromGeom(self,extract_only_points_on_polyline,include_distance_variable,num_pts_to_extract_along_polyline,extract_to_file,extract_f_name):
  args=((ValueType.Scalar,c_bool,extract_only_points_on_polyline),
        (ValueType.Scalar,c_bool,include_distance_variable),
        (ValueType.Scalar,c_int64,num_pts_to_extract_along_polyline),
        (ValueType.Scalar,c_bool,extract_to_file),
        (ValueType.Text,None,extract_f_name),)
  rep=self.sndrcv("ExtractFromGeom",*args)
  self.chk(rep)
  return (rep.status == tecrpc.Reply.Success)
 def ExtractFromPolyline(self,polyline_x_pts_array,polyline_y_pts_array,polyline_z_pts_array,num_pts_in_polyline,extract_through_volume,extract_only_points_on_polyline,include_distance_variable,num_pts_to_extract_along_polyline,extract_to_file,extract_f_name):
  args=((ValueType.Array,c_double,polyline_x_pts_array),
        (ValueType.Array,c_double,polyline_y_pts_array),
        (ValueType.Array,c_double,polyline_z_pts_array),
        (ValueType.Scalar,c_int64,num_pts_in_polyline),
        (ValueType.Scalar,c_bool,extract_through_volume),
        (ValueType.Scalar,c_bool,extract_only_points_on_polyline),
        (ValueType.Scalar,c_bool,include_distance_variable),
        (ValueType.Scalar,c_int64,num_pts_to_extract_along_polyline),
        (ValueType.Scalar,c_bool,extract_to_file),
        (ValueType.Text,None,extract_f_name),)
  rep=self.sndrcv("ExtractFromPolyline",*args)
  self.chk(rep)
  return (rep.status == tecrpc.Reply.Success)
 def ExtractInstallCallback(self,extract_destination,information_line_text):
  args=((ValueType.Address,c_uint64,getattr(extract_destination,'value',extract_destination)),
        (ValueType.Text,None,information_line_text),)
  rep=self.sndrcv("ExtractInstallCallback",*args)
  self.chk(rep)
  return (rep.status == tecrpc.Reply.Success)
 def ExtractIsoSurfacesX(self,arg_list):
  args=((ValueType.Address,c_uint64,getattr(arg_list,'value',arg_list)),)
  rep=self.sndrcv("ExtractIsoSurfacesX",*args)
  self.chk(rep)
  return (rep.status == tecrpc.Reply.Success)
 def ExtractSlicesX(self,arg_list):
  args=((ValueType.Address,c_uint64,getattr(arg_list,'value',arg_list)),)
  rep=self.sndrcv("ExtractSlicesX",*args)
  self.chk(rep)
  return (rep.status == tecrpc.Reply.Success)
 def ExtractStreamtracesX(self,arg_list):
  args=((ValueType.Address,c_uint64,getattr(arg_list,'value',arg_list)),)
  rep=self.sndrcv("ExtractStreamtracesX",*args)
  self.chk(rep)
  return (rep.status == tecrpc.Reply.Success)
 def ExtractTimesFromFileNames(self,file_names,times,require_alpha_token_matching):
  args=((ValueType.Address,c_uint64,getattr(file_names,'value',file_names)),
        (ValueType.Array,c_double,times),
        (ValueType.Scalar,c_bool,require_alpha_token_matching),)
  rep=self.sndrcv("ExtractTimesFromFileNames",*args)
  self.chk(rep)
  memmove(times, rep.args[0].buffer, sizeof(times))
  return (rep.status == tecrpc.Reply.Success)
 def FeatureIsEnabled(self,feature_id):
  args=((ValueType.Scalar,c_uint64,feature_id),)
  rep=self.sndrcv("FeatureIsEnabled",*args)
  self.chk(rep)
  return (
   rep.args[0].boolean,
   self.read_text(rep.args[1]))
 def FieldLayerIsActive(self,layer_show_flag):
  args=((ValueType.Text,None,layer_show_flag),)
  rep=self.sndrcv("FieldLayerIsActive",*args)
  self.chk(rep)
  return rep.args[0].boolean
 def FieldLayerIsActiveForFrame(self,frame_id,layer_show_flag):
  args=((ValueType.Scalar,c_int64,frame_id),
        (ValueType.Text,None,layer_show_flag),)
  rep=self.sndrcv("FieldLayerIsActiveForFrame",*args)
  self.chk(rep)
  return rep.args[0].boolean
 def FieldLayerSetIsActive(self,layer_show_flag,turn_on_field_layer):
  args=((ValueType.Text,None,layer_show_flag),
        (ValueType.Scalar,c_bool,turn_on_field_layer),)
  rep=self.sndrcv("FieldLayerSetIsActive",*args)
  self.chk(rep)
  return try_cast_to_enum(SetValueReturnCode, rep.args[0].int32)
 def FieldMapGetActive(self):
  rep=self.sndrcv("FieldMapGetActive")
  self.chk(rep)
  return (
   (rep.status == tecrpc.Reply.Success),
   rep.args[0].uint64)
 def FieldMapGetCandidateZone(self,field_map):
  args=((ValueType.Scalar,c_int32,field_map),)
  rep=self.sndrcv("FieldMapGetCandidateZone",*args)
  self.chk(rep)
  return rep.args[0].int32
 def FieldMapGetCandidateZoneForFrame(self,frame_id,field_map):
  args=((ValueType.Scalar,c_int64,frame_id),
        (ValueType.Scalar,c_int32,field_map),)
  rep=self.sndrcv("FieldMapGetCandidateZoneForFrame",*args)
  self.chk(rep)
  return rep.args[0].int32
 def FieldMapGetCount(self):
  rep=self.sndrcv("FieldMapGetCount")
  self.chk(rep)
  return rep.args[0].int32
 def FieldMapGetCountForFrame(self,frame_id):
  args=((ValueType.Scalar,c_int64,frame_id),)
  rep=self.sndrcv("FieldMapGetCountForFrame",*args)
  self.chk(rep)
  return rep.args[0].int32
 def FieldMapGetMode(self,field_map):
  args=((ValueType.Scalar,c_int32,field_map),)
  rep=self.sndrcv("FieldMapGetMode",*args)
  self.chk(rep)
  return try_cast_to_enum(FieldMapMode, rep.args[0].int32)
 def FieldMapGetModeForFrame(self,frame_id,field_map):
  args=((ValueType.Scalar,c_int64,frame_id),
        (ValueType.Scalar,c_int32,field_map),)
  rep=self.sndrcv("FieldMapGetModeForFrame",*args)
  self.chk(rep)
  return try_cast_to_enum(FieldMapMode, rep.args[0].int32)
 def FieldMapGetZones(self,field_map):
  args=((ValueType.Scalar,c_int32,field_map),)
  rep=self.sndrcv("FieldMapGetZones",*args)
  self.chk(rep)
  return (
   (rep.status == tecrpc.Reply.Success),
   rep.args[0].uint64)
 def FieldMapHasFEZones(self,field_map):
  args=((ValueType.Scalar,c_int32,field_map),)
  rep=self.sndrcv("FieldMapHasFEZones",*args)
  self.chk(rep)
  return rep.args[0].boolean
 def FieldMapHasIJKOrderedZones(self,field_map):
  args=((ValueType.Scalar,c_int32,field_map),)
  rep=self.sndrcv("FieldMapHasIJKOrderedZones",*args)
  self.chk(rep)
  return rep.args[0].boolean
 def FieldMapHasIJKOrderedZonesForFrame(self,frame_id,field_map):
  args=((ValueType.Scalar,c_int64,frame_id),
        (ValueType.Scalar,c_int32,field_map),)
  rep=self.sndrcv("FieldMapHasIJKOrderedZonesForFrame",*args)
  self.chk(rep)
  return rep.args[0].boolean
 def FieldMapHasLinearZones(self,field_map):
  args=((ValueType.Scalar,c_int32,field_map),)
  rep=self.sndrcv("FieldMapHasLinearZones",*args)
  self.chk(rep)
  return rep.args[0].boolean
 def FieldMapHasOrderedZones(self,field_map):
  args=((ValueType.Scalar,c_int32,field_map),)
  rep=self.sndrcv("FieldMapHasOrderedZones",*args)
  self.chk(rep)
  return rep.args[0].boolean
 def FieldMapHasOrderedZonesForFrame(self,frame_id,field_map):
  args=((ValueType.Scalar,c_int64,frame_id),
        (ValueType.Scalar,c_int32,field_map),)
  rep=self.sndrcv("FieldMapHasOrderedZonesForFrame",*args)
  self.chk(rep)
  return rep.args[0].boolean
 def FieldMapHasSurfaceZones(self,field_map):
  args=((ValueType.Scalar,c_int32,field_map),)
  rep=self.sndrcv("FieldMapHasSurfaceZones",*args)
  self.chk(rep)
  return rep.args[0].boolean
 def FieldMapHasVolumeZones(self,field_map):
  args=((ValueType.Scalar,c_int32,field_map),)
  rep=self.sndrcv("FieldMapHasVolumeZones",*args)
  self.chk(rep)
  return rep.args[0].boolean
 def FieldMapHasVolumeZonesForFrame(self,frame_id,field_map):
  args=((ValueType.Scalar,c_int64,frame_id),
        (ValueType.Scalar,c_int32,field_map),)
  rep=self.sndrcv("FieldMapHasVolumeZonesForFrame",*args)
  self.chk(rep)
  return rep.args[0].boolean
 def FieldMapIsActive(self,field_map):
  args=((ValueType.Scalar,c_int32,field_map),)
  rep=self.sndrcv("FieldMapIsActive",*args)
  self.chk(rep)
  return rep.args[0].boolean
 def FieldMapIsActiveForFrame(self,frame_id,field_map):
  args=((ValueType.Scalar,c_int64,frame_id),
        (ValueType.Scalar,c_int32,field_map),)
  rep=self.sndrcv("FieldMapIsActiveForFrame",*args)
  self.chk(rep)
  return rep.args[0].boolean
 def FieldMapIsRelevant(self,field_map):
  args=((ValueType.Scalar,c_int32,field_map),)
  rep=self.sndrcv("FieldMapIsRelevant",*args)
  self.chk(rep)
  return rep.args[0].boolean
 def FieldMapSetActive(self,field_map_set,assign_modifier):
  args=((ValueType.Address,c_uint64,getattr(field_map_set,'value',field_map_set)),
        (ValueType.Scalar,c_int32,AssignOp(assign_modifier).value),)
  rep=self.sndrcv("FieldMapSetActive",*args)
  self.chk(rep)
  return try_cast_to_enum(SetValueReturnCode, rep.args[0].int32)
 def FieldStyleGetArbValue(self,zone,s1,s2,s3):
  args=((ValueType.Scalar,c_int32,zone),
        (ValueType.Text,None,s1),
        (ValueType.Text,None,s2),
        (ValueType.Text,None,s3),)
  rep=self.sndrcv("FieldStyleGetArbValue",*args)
  self.chk(rep)
  return self.read_arbparam(rep.args[0])
 def FieldStyleGetDoubleValue(self,zone,s1,s2,s3):
  args=((ValueType.Scalar,c_int32,zone),
        (ValueType.Text,None,s1),
        (ValueType.Text,None,s2),
        (ValueType.Text,None,s3),)
  rep=self.sndrcv("FieldStyleGetDoubleValue",*args)
  self.chk(rep)
  return rep.args[0].float64
 def FileGetTempDirName(self):
  rep=self.sndrcv("FileGetTempDirName")
  self.chk(rep)
  return (
   (rep.status == tecrpc.Reply.Success),
   self.read_text(rep.args[0]))
 def FileGetTempName(self):
  rep=self.sndrcv("FileGetTempName")
  self.chk(rep)
  return (
   (rep.status == tecrpc.Reply.Success),
   self.read_text(rep.args[0]))
 def FormatTimeDateString(self,input_date,formatting_mask):
  args=((ValueType.Scalar,c_double,input_date),
        (ValueType.Text,None,formatting_mask),)
  rep=self.sndrcv("FormatTimeDateString",*args)
  self.chk(rep)
  return (
   (rep.status == tecrpc.Reply.Success),
   self.read_text(rep.args[0]))
 def FourierTransform(self,independent_var,window_function,dependent_vars,source_zones,include_conjugates,obey_source_zone_blanking):
  args=((ValueType.Scalar,c_int32,independent_var),
        (ValueType.Scalar,c_int32,WindowFunction(window_function).value),
        (ValueType.Address,c_uint64,getattr(dependent_vars,'value',dependent_vars)),
        (ValueType.Address,c_uint64,getattr(source_zones,'value',source_zones)),
        (ValueType.Scalar,c_bool,include_conjugates),
        (ValueType.Scalar,c_bool,obey_source_zone_blanking),)
  rep=self.sndrcv("FourierTransform",*args)
  self.chk(rep)
  return (rep.status == tecrpc.Reply.Success)
 def FourierTransformIsValidZone(self,zone_num):
  args=((ValueType.Scalar,c_int32,zone_num),)
  rep=self.sndrcv("FourierTransformIsValidZone",*args)
  self.chk(rep)
  return rep.args[0].boolean
 def FourierTransformIsValidZoneByDataSetID(self,dataset_id,zone_num):
  args=((ValueType.Scalar,c_int64,dataset_id),
        (ValueType.Scalar,c_int32,zone_num),)
  rep=self.sndrcv("FourierTransformIsValidZoneByDataSetID",*args)
  self.chk(rep)
  return rep.args[0].boolean
 def FourierTransformX(self,arg_list):
  args=((ValueType.Address,c_uint64,getattr(arg_list,'value',arg_list)),)
  rep=self.sndrcv("FourierTransformX",*args)
  self.chk(rep)
  return (rep.status == tecrpc.Reply.Success)
 def FrameActivateAtPosition(self,x,y):
  args=((ValueType.Scalar,c_double,x),
        (ValueType.Scalar,c_double,y),)
  rep=self.sndrcv("FrameActivateAtPosition",*args)
  self.chk(rep)
  return (rep.status == tecrpc.Reply.Success)
 def FrameActivateByName(self,name):
  args=((ValueType.Text,None,name),)
  rep=self.sndrcv("FrameActivateByName",*args)
  self.chk(rep)
  return (rep.status == tecrpc.Reply.Success)
 def FrameActivateByNumber(self,frame_num):
  args=((ValueType.Scalar,c_int32,frame_num),)
  rep=self.sndrcv("FrameActivateByNumber",*args)
  self.chk(rep)
  return (rep.status == tecrpc.Reply.Success)
 def FrameActivateByUniqueID(self,unique_id):
  args=((ValueType.Scalar,c_int64,unique_id),)
  rep=self.sndrcv("FrameActivateByUniqueID",*args)
  self.chk(rep)
  return (rep.status == tecrpc.Reply.Success)
 def FrameActivateTop(self):
  rep=self.sndrcv("FrameActivateTop")
  self.chk(rep)
  return (rep.status == tecrpc.Reply.Success)
 def FrameCreateNew(self,use_supplied_frame_size,x_pos,y_pos,width,height):
  args=((ValueType.Scalar,c_bool,use_supplied_frame_size),
        (ValueType.Scalar,c_double,x_pos),
        (ValueType.Scalar,c_double,y_pos),
        (ValueType.Scalar,c_double,width),
        (ValueType.Scalar,c_double,height),)
  rep=self.sndrcv("FrameCreateNew",*args)
  self.chk(rep)
  return (rep.status == tecrpc.Reply.Success)
 def FrameDeleteActive(self):
  rep=self.sndrcv("FrameDeleteActive")
  self.chk(rep)
  return (rep.status == tecrpc.Reply.Success)
 def FrameDeleteByNumber(self,frame_num):
  args=((ValueType.Scalar,c_int32,frame_num),)
  rep=self.sndrcv("FrameDeleteByNumber",*args)
  self.chk(rep)
  return (rep.status == tecrpc.Reply.Success)
 def FrameDeleteByUniqueID(self,unique_id):
  args=((ValueType.Scalar,c_int64,unique_id),)
  rep=self.sndrcv("FrameDeleteByUniqueID",*args)
  self.chk(rep)
  return (rep.status == tecrpc.Reply.Success)
 def FrameFitAllToPaper(self):
  rep=self.sndrcv("FrameFitAllToPaper")
  self.chk(rep)
  return (rep.status == tecrpc.Reply.Success)
 def FrameGetActiveID(self):
  rep=self.sndrcv("FrameGetActiveID")
  self.chk(rep)
  return rep.args[0].int64
 def FrameGetBackgroundColor(self):
  rep=self.sndrcv("FrameGetBackgroundColor")
  self.chk(rep)
  return rep.args[0].int32
 def FrameGetCount(self):
  rep=self.sndrcv("FrameGetCount")
  self.chk(rep)
  return rep.args[0].int32
 def FrameGetDataSetUniqueIDByFrameID(self,frame_id):
  args=((ValueType.Scalar,c_int64,frame_id),)
  rep=self.sndrcv("FrameGetDataSetUniqueIDByFrameID",*args)
  self.chk(rep)
  return rep.args[0].int64
 def FrameGetName(self):
  rep=self.sndrcv("FrameGetName")
  self.chk(rep)
  return (
   (rep.status == tecrpc.Reply.Success),
   self.read_text(rep.args[0]))
 def FrameGetPlotType(self):
  rep=self.sndrcv("FrameGetPlotType")
  self.chk(rep)
  return try_cast_to_enum(PlotType, rep.args[0].int32)
 def FrameGetPlotTypeForFrame(self,frame_id):
  args=((ValueType.Scalar,c_int64,frame_id),)
  rep=self.sndrcv("FrameGetPlotTypeForFrame",*args)
  self.chk(rep)
  return try_cast_to_enum(PlotType, rep.args[0].int32)
 def FrameGetPosAndSize(self):
  rep=self.sndrcv("FrameGetPosAndSize")
  self.chk(rep)
  return (
   rep.args[0].float64,
   rep.args[1].float64,
   rep.args[2].float64,
   rep.args[3].float64)
 def FrameGetUniqueID(self):
  rep=self.sndrcv("FrameGetUniqueID")
  self.chk(rep)
  return rep.args[0].int64
 def FrameLightweightForAllPagesLoopEnd(self):
  rep=self.sndrcv("FrameLightweightForAllPagesLoopEnd")
  self.chk(rep)
 def FrameLightweightForAllPagesLoopNext(self):
  rep=self.sndrcv("FrameLightweightForAllPagesLoopNext")
  self.chk(rep)
  return (rep.status == tecrpc.Reply.Success)
 def FrameLightweightForAllPagesLoopStart(self):
  rep=self.sndrcv("FrameLightweightForAllPagesLoopStart")
  self.chk(rep)
 def FrameLightweightLoopEnd(self):
  rep=self.sndrcv("FrameLightweightLoopEnd")
  self.chk(rep)
 def FrameLightweightLoopNext(self):
  rep=self.sndrcv("FrameLightweightLoopNext")
  self.chk(rep)
  return rep.args[0].boolean
 def FrameLightweightLoopStart(self):
  rep=self.sndrcv("FrameLightweightLoopStart")
  self.chk(rep)
 def FrameManagesTransientData(self):
  rep=self.sndrcv("FrameManagesTransientData")
  self.chk(rep)
  return (rep.status == tecrpc.Reply.Success)
 def FrameMoveToBottomByName(self,name):
  args=((ValueType.Text,None,name),)
  rep=self.sndrcv("FrameMoveToBottomByName",*args)
  self.chk(rep)
  return (rep.status == tecrpc.Reply.Success)
 def FrameMoveToBottomByNumber(self,frame_num):
  args=((ValueType.Scalar,c_int32,frame_num),)
  rep=self.sndrcv("FrameMoveToBottomByNumber",*args)
  self.chk(rep)
  return (rep.status == tecrpc.Reply.Success)
 def FrameMoveToBottomByUniqueID(self,unique_id):
  args=((ValueType.Scalar,c_int64,unique_id),)
  rep=self.sndrcv("FrameMoveToBottomByUniqueID",*args)
  self.chk(rep)
  return (rep.status == tecrpc.Reply.Success)
 def FrameMoveToTopByName(self,name):
  args=((ValueType.Text,None,name),)
  rep=self.sndrcv("FrameMoveToTopByName",*args)
  self.chk(rep)
  return (rep.status == tecrpc.Reply.Success)
 def FrameMoveToTopByNumber(self,frame_num):
  args=((ValueType.Scalar,c_int32,frame_num),)
  rep=self.sndrcv("FrameMoveToTopByNumber",*args)
  self.chk(rep)
  return (rep.status == tecrpc.Reply.Success)
 def FrameMoveToTopByUniqueID(self,unique_id):
  args=((ValueType.Scalar,c_int64,unique_id),)
  rep=self.sndrcv("FrameMoveToTopByUniqueID",*args)
  self.chk(rep)
  return (rep.status == tecrpc.Reply.Success)
 def FrameNeedsRedraw(self,frame_id):
  args=((ValueType.Scalar,c_int64,frame_id),)
  rep=self.sndrcv("FrameNeedsRedraw",*args)
  self.chk(rep)
  return rep.args[0].boolean
 def FramePopAtPosition(self,x,y):
  args=((ValueType.Scalar,c_double,x),
        (ValueType.Scalar,c_double,y),)
  rep=self.sndrcv("FramePopAtPosition",*args)
  self.chk(rep)
  return (rep.status == tecrpc.Reply.Success)
 def FrameReset(self,frame_id):
  args=((ValueType.Scalar,c_int64,frame_id),)
  rep=self.sndrcv("FrameReset",*args)
  self.chk(rep)
 def FrameSetBackgroundColor(self,color):
  args=((ValueType.Scalar,c_int32,color),)
  rep=self.sndrcv("FrameSetBackgroundColor",*args)
  self.chk(rep)
  return try_cast_to_enum(SetValueReturnCode, rep.args[0].int32)
 def FrameSetDataSet(self,source_data_set_id,target_frame_id):
  args=((ValueType.Scalar,c_int64,source_data_set_id),
        (ValueType.Scalar,c_int64,target_frame_id),)
  rep=self.sndrcv("FrameSetDataSet",*args)
  self.chk(rep)
  return (rep.status == tecrpc.Reply.Success)
 def FrameSetName(self,name):
  args=((ValueType.Text,None,name),)
  rep=self.sndrcv("FrameSetName",*args)
  self.chk(rep)
  return try_cast_to_enum(SetValueReturnCode, rep.args[0].int32)
 def FrameSetNumberByUniqueID(self,unique_id,new_number):
  args=((ValueType.Scalar,c_int64,unique_id),
        (ValueType.Scalar,c_int32,new_number),)
  rep=self.sndrcv("FrameSetNumberByUniqueID",*args)
  self.chk(rep)
  return (rep.status == tecrpc.Reply.Success)
 def FrameSetPlotType(self,new_plot_type):
  args=((ValueType.Scalar,c_int32,PlotType(new_plot_type).value),)
  rep=self.sndrcv("FrameSetPlotType",*args)
  self.chk(rep)
  return try_cast_to_enum(SetValueReturnCode, rep.args[0].int32)
 def FrameSetPosAndSize(self,x,y,width,height):
  args=((ValueType.Scalar,c_double,x),
        (ValueType.Scalar,c_double,y),
        (ValueType.Scalar,c_double,width),
        (ValueType.Scalar,c_double,height),)
  rep=self.sndrcv("FrameSetPosAndSize",*args)
  self.chk(rep)
  return try_cast_to_enum(SetValueReturnCode, rep.args[0].int32)
 def GeoRefImageCreate(self,image_fle_name,world_file_name):
  args=((ValueType.Text,None,image_fle_name),
        (ValueType.Text,None,world_file_name),)
  rep=self.sndrcv("GeoRefImageCreate",*args)
  self.chk(rep)
  return rep.args[0].int64
 def Geom2DLineSegmentCreate(self,position_coord_sys,x1,y1,x2,y2):
  args=((ValueType.Scalar,c_int32,CoordSys(position_coord_sys).value),
        (ValueType.Scalar,c_double,x1),
        (ValueType.Scalar,c_double,y1),
        (ValueType.Scalar,c_double,x2),
        (ValueType.Scalar,c_double,y2),)
  rep=self.sndrcv("Geom2DLineSegmentCreate",*args)
  self.chk(rep)
  return rep.args[0].int64
 def Geom2DMPolyCreate(self,position_coord_sys,num_polys,num_points_in_polylines_array):
  args=((ValueType.Scalar,c_int32,CoordSys(position_coord_sys).value),
        (ValueType.Scalar,c_int32,num_polys),
        (ValueType.Array,c_int64,num_points_in_polylines_array),)
  rep=self.sndrcv("Geom2DMPolyCreate",*args)
  self.chk(rep)
  return rep.args[0].int64
 def Geom2DMPolyGetPoint(self,gid,poly_num,point_index):
  args=((ValueType.Scalar,c_int64,gid),
        (ValueType.Scalar,c_int32,poly_num),
        (ValueType.Scalar,c_int64,point_index),)
  rep=self.sndrcv("Geom2DMPolyGetPoint",*args)
  self.chk(rep)
  return (
   rep.args[0].float64,
   rep.args[1].float64)
 def Geom2DMPolySetPoint(self,gid,poly_num,point_index,x,y):
  args=((ValueType.Scalar,c_int64,gid),
        (ValueType.Scalar,c_int32,poly_num),
        (ValueType.Scalar,c_int64,point_index),
        (ValueType.Scalar,c_double,x),
        (ValueType.Scalar,c_double,y),)
  rep=self.sndrcv("Geom2DMPolySetPoint",*args)
  self.chk(rep)
 def Geom2DMPolySetPolyline(self,gid,poly_num,x_array,y_array):
  args=((ValueType.Scalar,c_int64,gid),
        (ValueType.Scalar,c_int32,poly_num),
        (ValueType.Array,c_double,x_array),
        (ValueType.Array,c_double,y_array),)
  rep=self.sndrcv("Geom2DMPolySetPolyline",*args)
  self.chk(rep)
 def Geom2DPolylineCreate(self,position_coord_sys,pts_x_array,pts_y_array,num_pts):
  args=((ValueType.Scalar,c_int32,CoordSys(position_coord_sys).value),
        (ValueType.Array,c_double,pts_x_array),
        (ValueType.Array,c_double,pts_y_array),
        (ValueType.Scalar,c_int64,num_pts),)
  rep=self.sndrcv("Geom2DPolylineCreate",*args)
  self.chk(rep)
  return rep.args[0].int64
 def Geom2DPolylineGetPoint(self,gid,point_index):
  args=((ValueType.Scalar,c_int64,gid),
        (ValueType.Scalar,c_int64,point_index),)
  rep=self.sndrcv("Geom2DPolylineGetPoint",*args)
  self.chk(rep)
  return (
   rep.args[0].float64,
   rep.args[1].float64)
 def Geom2DPolylineSetPoint(self,gid,point_index,x,y):
  args=((ValueType.Scalar,c_int64,gid),
        (ValueType.Scalar,c_int64,point_index),
        (ValueType.Scalar,c_double,x),
        (ValueType.Scalar,c_double,y),)
  rep=self.sndrcv("Geom2DPolylineSetPoint",*args)
  self.chk(rep)
 def Geom3DLineSegmentCreate(self,x1,y1,z1,x2,y2,z2):
  args=((ValueType.Scalar,c_double,x1),
        (ValueType.Scalar,c_double,y1),
        (ValueType.Scalar,c_double,z1),
        (ValueType.Scalar,c_double,x2),
        (ValueType.Scalar,c_double,y2),
        (ValueType.Scalar,c_double,z2),)
  rep=self.sndrcv("Geom3DLineSegmentCreate",*args)
  self.chk(rep)
  return rep.args[0].int64
 def Geom3DMPolyCreate(self,num_polys,num_points_in_polylines_array):
  args=((ValueType.Scalar,c_int32,num_polys),
        (ValueType.Array,c_int64,num_points_in_polylines_array),)
  rep=self.sndrcv("Geom3DMPolyCreate",*args)
  self.chk(rep)
  return rep.args[0].int64
 def Geom3DMPolyGetPoint(self,gid,poly_num,point_index):
  args=((ValueType.Scalar,c_int64,gid),
        (ValueType.Scalar,c_int32,poly_num),
        (ValueType.Scalar,c_int64,point_index),)
  rep=self.sndrcv("Geom3DMPolyGetPoint",*args)
  self.chk(rep)
  return (
   rep.args[0].float64,
   rep.args[1].float64,
   rep.args[2].float64)
 def Geom3DMPolySetPoint(self,gid,poly_num,point_index,x,y,z):
  args=((ValueType.Scalar,c_int64,gid),
        (ValueType.Scalar,c_int32,poly_num),
        (ValueType.Scalar,c_int64,point_index),
        (ValueType.Scalar,c_double,x),
        (ValueType.Scalar,c_double,y),
        (ValueType.Scalar,c_double,z),)
  rep=self.sndrcv("Geom3DMPolySetPoint",*args)
  self.chk(rep)
 def Geom3DMPolySetPolyline(self,gid,poly_num,x_array,y_array,z_array):
  args=((ValueType.Scalar,c_int64,gid),
        (ValueType.Scalar,c_int32,poly_num),
        (ValueType.Array,c_double,x_array),
        (ValueType.Array,c_double,y_array),
        (ValueType.Array,c_double,z_array),)
  rep=self.sndrcv("Geom3DMPolySetPolyline",*args)
  self.chk(rep)
 def Geom3DPolylineCreate(self,pts_x_array,pts_y_array,pts_z_array,num_pts):
  args=((ValueType.Array,c_double,pts_x_array),
        (ValueType.Array,c_double,pts_y_array),
        (ValueType.Array,c_double,pts_z_array),
        (ValueType.Scalar,c_int64,num_pts),)
  rep=self.sndrcv("Geom3DPolylineCreate",*args)
  self.chk(rep)
  return rep.args[0].int64
 def Geom3DPolylineGetPoint(self,gid,point_index):
  args=((ValueType.Scalar,c_int64,gid),
        (ValueType.Scalar,c_int64,point_index),)
  rep=self.sndrcv("Geom3DPolylineGetPoint",*args)
  self.chk(rep)
  return (
   rep.args[0].float64,
   rep.args[1].float64,
   rep.args[2].float64)
 def Geom3DPolylineSetPoint(self,gid,point_index,x,y,z):
  args=((ValueType.Scalar,c_int64,gid),
        (ValueType.Scalar,c_int64,point_index),
        (ValueType.Scalar,c_double,x),
        (ValueType.Scalar,c_double,y),
        (ValueType.Scalar,c_double,z),)
  rep=self.sndrcv("Geom3DPolylineSetPoint",*args)
  self.chk(rep)
 def GeomArcCreate(self,position_coord_sys,center_x,center_y,radius,start_angle,end_angle):
  args=((ValueType.Scalar,c_int32,CoordSys(position_coord_sys).value),
        (ValueType.Scalar,c_double,center_x),
        (ValueType.Scalar,c_double,center_y),
        (ValueType.Scalar,c_double,radius),
        (ValueType.Scalar,c_double,start_angle),
        (ValueType.Scalar,c_double,end_angle),)
  rep=self.sndrcv("GeomArcCreate",*args)
  self.chk(rep)
  return rep.args[0].int64
 def GeomArrowheadGetAngle(self,gid):
  args=((ValueType.Scalar,c_int64,gid),)
  rep=self.sndrcv("GeomArrowheadGetAngle",*args)
  self.chk(rep)
  return rep.args[0].float64
 def GeomArrowheadGetAttach(self,gid):
  args=((ValueType.Scalar,c_int64,gid),)
  rep=self.sndrcv("GeomArrowheadGetAttach",*args)
  self.chk(rep)
  return try_cast_to_enum(ArrowheadAttachment, rep.args[0].int32)
 def GeomArrowheadGetSize(self,gid):
  args=((ValueType.Scalar,c_int64,gid),)
  rep=self.sndrcv("GeomArrowheadGetSize",*args)
  self.chk(rep)
  return rep.args[0].float64
 def GeomArrowheadGetStyle(self,gid):
  args=((ValueType.Scalar,c_int64,gid),)
  rep=self.sndrcv("GeomArrowheadGetStyle",*args)
  self.chk(rep)
  return try_cast_to_enum(ArrowheadStyle, rep.args[0].int32)
 def GeomArrowheadSetAngle(self,gid,arrowhead_angle):
  args=((ValueType.Scalar,c_int64,gid),
        (ValueType.Scalar,c_double,arrowhead_angle),)
  rep=self.sndrcv("GeomArrowheadSetAngle",*args)
  self.chk(rep)
 def GeomArrowheadSetAttach(self,gid,arrowhead_attachment):
  args=((ValueType.Scalar,c_int64,gid),
        (ValueType.Scalar,c_int32,ArrowheadAttachment(arrowhead_attachment).value),)
  rep=self.sndrcv("GeomArrowheadSetAttach",*args)
  self.chk(rep)
 def GeomArrowheadSetSize(self,gid,arrowhead_size):
  args=((ValueType.Scalar,c_int64,gid),
        (ValueType.Scalar,c_double,arrowhead_size),)
  rep=self.sndrcv("GeomArrowheadSetSize",*args)
  self.chk(rep)
 def GeomArrowheadSetStyle(self,gid,arrowhead_style):
  args=((ValueType.Scalar,c_int64,gid),
        (ValueType.Scalar,c_int32,ArrowheadStyle(arrowhead_style).value),)
  rep=self.sndrcv("GeomArrowheadSetStyle",*args)
  self.chk(rep)
 def GeomCircleCreate(self,position_coord_sys,center_x,center_y,radius):
  args=((ValueType.Scalar,c_int32,CoordSys(position_coord_sys).value),
        (ValueType.Scalar,c_double,center_x),
        (ValueType.Scalar,c_double,center_y),
        (ValueType.Scalar,c_double,radius),)
  rep=self.sndrcv("GeomCircleCreate",*args)
  self.chk(rep)
  return rep.args[0].int64
 def GeomCircleGetRadius(self,gid):
  args=((ValueType.Scalar,c_int64,gid),)
  rep=self.sndrcv("GeomCircleGetRadius",*args)
  self.chk(rep)
  return rep.args[0].float64
 def GeomCircleSetRadius(self,gid,radius):
  args=((ValueType.Scalar,c_int64,gid),
        (ValueType.Scalar,c_double,radius),)
  rep=self.sndrcv("GeomCircleSetRadius",*args)
  self.chk(rep)
 def GeomDelete(self,gid):
  args=((ValueType.Scalar,c_int64,gid),)
  rep=self.sndrcv("GeomDelete",*args)
  self.chk(rep)
 def GeomEllipseCreate(self,position_coord_sys,center_x,center_y,h_axis,v_axis):
  args=((ValueType.Scalar,c_int32,CoordSys(position_coord_sys).value),
        (ValueType.Scalar,c_double,center_x),
        (ValueType.Scalar,c_double,center_y),
        (ValueType.Scalar,c_double,h_axis),
        (ValueType.Scalar,c_double,v_axis),)
  rep=self.sndrcv("GeomEllipseCreate",*args)
  self.chk(rep)
  return rep.args[0].int64
 def GeomEllipseGetNumPoints(self,gid):
  args=((ValueType.Scalar,c_int64,gid),)
  rep=self.sndrcv("GeomEllipseGetNumPoints",*args)
  self.chk(rep)
  return rep.args[0].int32
 def GeomEllipseGetSize(self,gid):
  args=((ValueType.Scalar,c_int64,gid),)
  rep=self.sndrcv("GeomEllipseGetSize",*args)
  self.chk(rep)
  return (
   rep.args[0].float64,
   rep.args[1].float64)
 def GeomEllipseSetNumPoints(self,gid,num_ellipse_pts):
  args=((ValueType.Scalar,c_int64,gid),
        (ValueType.Scalar,c_int32,num_ellipse_pts),)
  rep=self.sndrcv("GeomEllipseSetNumPoints",*args)
  self.chk(rep)
 def GeomEllipseSetSize(self,gid,h_axis,v_axis):
  args=((ValueType.Scalar,c_int64,gid),
        (ValueType.Scalar,c_double,h_axis),
        (ValueType.Scalar,c_double,v_axis),)
  rep=self.sndrcv("GeomEllipseSetSize",*args)
  self.chk(rep)
 def GeomGetAnchorPos(self,gid):
  args=((ValueType.Scalar,c_int64,gid),)
  rep=self.sndrcv("GeomGetAnchorPos",*args)
  self.chk(rep)
  return (
   rep.args[0].float64,
   rep.args[1].float64,
   rep.args[2].float64)
 def GeomGetBase(self):
  rep=self.sndrcv("GeomGetBase")
  self.chk(rep)
  return rep.args[0].int64
 def GeomGetClipping(self,gid):
  args=((ValueType.Scalar,c_int64,gid),)
  rep=self.sndrcv("GeomGetClipping",*args)
  self.chk(rep)
  return try_cast_to_enum(Clipping, rep.args[0].int32)
 def GeomGetColor(self,gid):
  args=((ValueType.Scalar,c_int64,gid),)
  rep=self.sndrcv("GeomGetColor",*args)
  self.chk(rep)
  return rep.args[0].int32
 def GeomGetDrawOrder(self,gid):
  args=((ValueType.Scalar,c_int64,gid),)
  rep=self.sndrcv("GeomGetDrawOrder",*args)
  self.chk(rep)
  return try_cast_to_enum(DrawOrder, rep.args[0].int32)
 def GeomGetFillColor(self,gid):
  args=((ValueType.Scalar,c_int64,gid),)
  rep=self.sndrcv("GeomGetFillColor",*args)
  self.chk(rep)
  return rep.args[0].int32
 def GeomGetIsFilled(self,gid):
  args=((ValueType.Scalar,c_int64,gid),)
  rep=self.sndrcv("GeomGetIsFilled",*args)
  self.chk(rep)
  return rep.args[0].boolean
 def GeomGetLinePattern(self,gid):
  args=((ValueType.Scalar,c_int64,gid),)
  rep=self.sndrcv("GeomGetLinePattern",*args)
  self.chk(rep)
  return try_cast_to_enum(LinePattern, rep.args[0].int32)
 def GeomGetLineThickness(self,gid):
  args=((ValueType.Scalar,c_int64,gid),)
  rep=self.sndrcv("GeomGetLineThickness",*args)
  self.chk(rep)
  return rep.args[0].float64
 def GeomGetMacroFunctionCmd(self,gid):
  args=((ValueType.Scalar,c_int64,gid),)
  rep=self.sndrcv("GeomGetMacroFunctionCmd",*args)
  self.chk(rep)
  return (
   (rep.status == tecrpc.Reply.Success),
   self.read_text(rep.args[0]))
 def GeomGetNext(self,gid):
  args=((ValueType.Scalar,c_int64,gid),)
  rep=self.sndrcv("GeomGetNext",*args)
  self.chk(rep)
  return rep.args[0].int64
 def GeomGetPatternLength(self,gid):
  args=((ValueType.Scalar,c_int64,gid),)
  rep=self.sndrcv("GeomGetPatternLength",*args)
  self.chk(rep)
  return rep.args[0].float64
 def GeomGetPositionCoordSys(self,gid):
  args=((ValueType.Scalar,c_int64,gid),)
  rep=self.sndrcv("GeomGetPositionCoordSys",*args)
  self.chk(rep)
  return try_cast_to_enum(CoordSys, rep.args[0].int32)
 def GeomGetPrev(self,gid):
  args=((ValueType.Scalar,c_int64,gid),)
  rep=self.sndrcv("GeomGetPrev",*args)
  self.chk(rep)
  return rep.args[0].int64
 def GeomGetScope(self,gid):
  args=((ValueType.Scalar,c_int64,gid),)
  rep=self.sndrcv("GeomGetScope",*args)
  self.chk(rep)
  return try_cast_to_enum(Scope, rep.args[0].int32)
 def GeomGetType(self,gid):
  args=((ValueType.Scalar,c_int64,gid),)
  rep=self.sndrcv("GeomGetType",*args)
  self.chk(rep)
  return try_cast_to_enum(GeomType, rep.args[0].int32)
 def GeomGetZoneOrMap(self,gid):
  args=((ValueType.Scalar,c_int64,gid),)
  rep=self.sndrcv("GeomGetZoneOrMap",*args)
  self.chk(rep)
  return rep.args[0].int32
 def GeomImageCreate(self,f_name,x_pos,y_pos,size):
  args=((ValueType.Text,None,f_name),
        (ValueType.Scalar,c_double,x_pos),
        (ValueType.Scalar,c_double,y_pos),
        (ValueType.Scalar,c_double,size),)
  rep=self.sndrcv("GeomImageCreate",*args)
  self.chk(rep)
  return rep.args[0].int64
 def GeomImageGetFileName(self,gid):
  args=((ValueType.Scalar,c_int64,gid),)
  rep=self.sndrcv("GeomImageGetFileName",*args)
  self.chk(rep)
  return self.read_text(rep.args[0])
 def GeomImageGetImage(self,gid):
  args=((ValueType.Scalar,c_int64,gid),)
  rep=self.sndrcv("GeomImageGetImage",*args)
  self.chk(rep)
  return (
   (rep.status == tecrpc.Reply.Success),
   rep.args[0].int32,
   rep.args[1].int32,
   self.read_array(rep.args[2], c_uint8))
 def GeomImageGetRawSize(self,gid):
  args=((ValueType.Scalar,c_int64,gid),)
  rep=self.sndrcv("GeomImageGetRawSize",*args)
  self.chk(rep)
  return (
   rep.args[0].float64,
   rep.args[1].float64)
 def GeomImageGetResizeFilter(self,gid):
  args=((ValueType.Scalar,c_int64,gid),)
  rep=self.sndrcv("GeomImageGetResizeFilter",*args)
  self.chk(rep)
  return try_cast_to_enum(ImageResizeFilter, rep.args[0].int32)
 def GeomImageGetSize(self,gid):
  args=((ValueType.Scalar,c_int64,gid),)
  rep=self.sndrcv("GeomImageGetSize",*args)
  self.chk(rep)
  return (
   rep.args[0].float64,
   rep.args[1].float64)
 def GeomImageGetUseRatio(self,gid):
  args=((ValueType.Scalar,c_int64,gid),)
  rep=self.sndrcv("GeomImageGetUseRatio",*args)
  self.chk(rep)
  return rep.args[0].boolean
 def GeomImageResetAspectRatio(self,gid):
  args=((ValueType.Scalar,c_int64,gid),)
  rep=self.sndrcv("GeomImageResetAspectRatio",*args)
  self.chk(rep)
 def GeomImageSetHeight(self,gid,height):
  args=((ValueType.Scalar,c_int64,gid),
        (ValueType.Scalar,c_double,height),)
  rep=self.sndrcv("GeomImageSetHeight",*args)
  self.chk(rep)
 def GeomImageSetResizeFilter(self,gid,resize_filter):
  args=((ValueType.Scalar,c_int64,gid),
        (ValueType.Scalar,c_int32,ImageResizeFilter(resize_filter).value),)
  rep=self.sndrcv("GeomImageSetResizeFilter",*args)
  self.chk(rep)
 def GeomImageSetUseRatio(self,gid,maintain_aspect_ratio):
  args=((ValueType.Scalar,c_int64,gid),
        (ValueType.Scalar,c_bool,maintain_aspect_ratio),)
  rep=self.sndrcv("GeomImageSetUseRatio",*args)
  self.chk(rep)
 def GeomImageSetWidth(self,gid,width):
  args=((ValueType.Scalar,c_int64,gid),
        (ValueType.Scalar,c_double,width),)
  rep=self.sndrcv("GeomImageSetWidth",*args)
  self.chk(rep)
 def GeomIsAttached(self,gid):
  args=((ValueType.Scalar,c_int64,gid),)
  rep=self.sndrcv("GeomIsAttached",*args)
  self.chk(rep)
  return rep.args[0].boolean
 def GeomIsValid(self,gid):
  args=((ValueType.Scalar,c_int64,gid),)
  rep=self.sndrcv("GeomIsValid",*args)
  self.chk(rep)
  return rep.args[0].boolean
 def GeomMPolyGetPointCount(self,gid,poly_num):
  args=((ValueType.Scalar,c_int64,gid),
        (ValueType.Scalar,c_int32,poly_num),)
  rep=self.sndrcv("GeomMPolyGetPointCount",*args)
  self.chk(rep)
  return rep.args[0].int64
 def GeomMPolyGetPolylineCnt(self,gid):
  args=((ValueType.Scalar,c_int64,gid),)
  rep=self.sndrcv("GeomMPolyGetPolylineCnt",*args)
  self.chk(rep)
  return rep.args[0].int64
 def GeomPolyGetPointCount(self,gid):
  args=((ValueType.Scalar,c_int64,gid),)
  rep=self.sndrcv("GeomPolyGetPointCount",*args)
  self.chk(rep)
  return rep.args[0].int64
 def GeomRectangleCreate(self,position_coord_sys,corner_x,corner_y,width,height):
  args=((ValueType.Scalar,c_int32,CoordSys(position_coord_sys).value),
        (ValueType.Scalar,c_double,corner_x),
        (ValueType.Scalar,c_double,corner_y),
        (ValueType.Scalar,c_double,width),
        (ValueType.Scalar,c_double,height),)
  rep=self.sndrcv("GeomRectangleCreate",*args)
  self.chk(rep)
  return rep.args[0].int64
 def GeomRectangleGetSize(self,gid):
  args=((ValueType.Scalar,c_int64,gid),)
  rep=self.sndrcv("GeomRectangleGetSize",*args)
  self.chk(rep)
  return (
   rep.args[0].float64,
   rep.args[1].float64)
 def GeomRectangleSetSize(self,gid,width,height):
  args=((ValueType.Scalar,c_int64,gid),
        (ValueType.Scalar,c_double,width),
        (ValueType.Scalar,c_double,height),)
  rep=self.sndrcv("GeomRectangleSetSize",*args)
  self.chk(rep)
 def GeomSetAnchorPos(self,gid,x_pos,y_pos,z_pos):
  args=((ValueType.Scalar,c_int64,gid),
        (ValueType.Scalar,c_double,x_pos),
        (ValueType.Scalar,c_double,y_pos),
        (ValueType.Scalar,c_double,z_pos),)
  rep=self.sndrcv("GeomSetAnchorPos",*args)
  self.chk(rep)
 def GeomSetAttached(self,gid,attached):
  args=((ValueType.Scalar,c_int64,gid),
        (ValueType.Scalar,c_bool,attached),)
  rep=self.sndrcv("GeomSetAttached",*args)
  self.chk(rep)
 def GeomSetClipping(self,gid,clipping):
  args=((ValueType.Scalar,c_int64,gid),
        (ValueType.Scalar,c_int32,Clipping(clipping).value),)
  rep=self.sndrcv("GeomSetClipping",*args)
  self.chk(rep)
 def GeomSetColor(self,gid,color):
  args=((ValueType.Scalar,c_int64,gid),
        (ValueType.Scalar,c_int32,color),)
  rep=self.sndrcv("GeomSetColor",*args)
  self.chk(rep)
 def GeomSetDrawOrder(self,gid,draw_order):
  args=((ValueType.Scalar,c_int64,gid),
        (ValueType.Scalar,c_int32,DrawOrder(draw_order).value),)
  rep=self.sndrcv("GeomSetDrawOrder",*args)
  self.chk(rep)
 def GeomSetFillColor(self,gid,fill_color):
  args=((ValueType.Scalar,c_int64,gid),
        (ValueType.Scalar,c_int32,fill_color),)
  rep=self.sndrcv("GeomSetFillColor",*args)
  self.chk(rep)
 def GeomSetIsFilled(self,gid,is_filled):
  args=((ValueType.Scalar,c_int64,gid),
        (ValueType.Scalar,c_bool,is_filled),)
  rep=self.sndrcv("GeomSetIsFilled",*args)
  self.chk(rep)
 def GeomSetLinePattern(self,gid,line_pattern):
  args=((ValueType.Scalar,c_int64,gid),
        (ValueType.Scalar,c_int32,LinePattern(line_pattern).value),)
  rep=self.sndrcv("GeomSetLinePattern",*args)
  self.chk(rep)
 def GeomSetLineThickness(self,gid,line_thickness):
  args=((ValueType.Scalar,c_int64,gid),
        (ValueType.Scalar,c_double,line_thickness),)
  rep=self.sndrcv("GeomSetLineThickness",*args)
  self.chk(rep)
 def GeomSetMacroFunctionCmd(self,gid,command):
  args=((ValueType.Scalar,c_int64,gid),
        (ValueType.Text,None,command),)
  rep=self.sndrcv("GeomSetMacroFunctionCmd",*args)
  self.chk(rep)
  return (rep.status == tecrpc.Reply.Success)
 def GeomSetPatternLength(self,gid,pattern_length):
  args=((ValueType.Scalar,c_int64,gid),
        (ValueType.Scalar,c_double,pattern_length),)
  rep=self.sndrcv("GeomSetPatternLength",*args)
  self.chk(rep)
 def GeomSetPositionCoordSys(self,gid,coord_sys):
  args=((ValueType.Scalar,c_int64,gid),
        (ValueType.Scalar,c_int32,CoordSys(coord_sys).value),)
  rep=self.sndrcv("GeomSetPositionCoordSys",*args)
  self.chk(rep)
 def GeomSetScope(self,gid,scope):
  args=((ValueType.Scalar,c_int64,gid),
        (ValueType.Scalar,c_int32,Scope(scope).value),)
  rep=self.sndrcv("GeomSetScope",*args)
  self.chk(rep)
 def GeomSetZoneOrMap(self,gid,zone_or_map):
  args=((ValueType.Scalar,c_int64,gid),
        (ValueType.Scalar,c_int32,zone_or_map),)
  rep=self.sndrcv("GeomSetZoneOrMap",*args)
  self.chk(rep)
 def GeomSquareCreate(self,position_coord_sys,corner_x,corner_y,size):
  args=((ValueType.Scalar,c_int32,CoordSys(position_coord_sys).value),
        (ValueType.Scalar,c_double,corner_x),
        (ValueType.Scalar,c_double,corner_y),
        (ValueType.Scalar,c_double,size),)
  rep=self.sndrcv("GeomSquareCreate",*args)
  self.chk(rep)
  return rep.args[0].int64
 def GeomSquareGetSize(self,gid):
  args=((ValueType.Scalar,c_int64,gid),)
  rep=self.sndrcv("GeomSquareGetSize",*args)
  self.chk(rep)
  return rep.args[0].float64
 def GeomSquareSetSize(self,gid,size):
  args=((ValueType.Scalar,c_int64,gid),
        (ValueType.Scalar,c_double,size),)
  rep=self.sndrcv("GeomSquareSetSize",*args)
  self.chk(rep)
 def GetBasePath(self,f_name):
  args=((ValueType.Text,None,f_name),)
  rep=self.sndrcv("GetBasePath",*args)
  self.chk(rep)
  return self.read_text(rep.args[0])
 def GetBoundingBoxOfAllFrames(self):
  rep=self.sndrcv("GetBoundingBoxOfAllFrames")
  self.chk(rep)
  return (
   rep.args[0].float64,
   rep.args[1].float64,
   rep.args[2].float64,
   rep.args[3].float64)
 def GetCurLayoutFName(self):
  rep=self.sndrcv("GetCurLayoutFName")
  self.chk(rep)
  return self.read_text(rep.args[0])
 def GetDefaultExportImageWidth(self,export_format,export_region):
  args=((ValueType.Scalar,c_int32,ExportFormat(export_format).value),
        (ValueType.Scalar,c_int32,ExportRegion(export_region).value),)
  rep=self.sndrcv("GetDefaultExportImageWidth",*args)
  self.chk(rep)
  return rep.args[0].int32
 def GetExportFormatExtensions(self,export_format):
  args=((ValueType.Scalar,c_int32,ExportFormat(export_format).value),)
  rep=self.sndrcv("GetExportFormatExtensions",*args)
  self.chk(rep)
  return (
   (rep.status == tecrpc.Reply.Success),
   self.read_text(rep.args[0]))
 def GetExportImageWidthAndHeight(self,export_region,export_format,width):
  args=((ValueType.Scalar,c_int32,ExportRegion(export_region).value),
        (ValueType.Scalar,c_int32,ExportFormat(export_format).value),
        (ValueType.Scalar,c_int32,width),)
  rep=self.sndrcv("GetExportImageWidthAndHeight",*args)
  self.chk(rep)
  return (
   rep.args[0].int32,
   rep.args[1].int32)
 def GetNextNiceIncDecValue(self,start_value,min_value,max_value,preferred_divisions,is_increasing):
  args=((ValueType.Scalar,c_double,start_value),
        (ValueType.Scalar,c_double,min_value),
        (ValueType.Scalar,c_double,max_value),
        (ValueType.Scalar,c_int64,preferred_divisions),
        (ValueType.Scalar,c_bool,is_increasing),)
  rep=self.sndrcv("GetNextNiceIncDecValue",*args)
  self.chk(rep)
  return rep.args[0].float64
 def GetNextUniqueID(self):
  rep=self.sndrcv("GetNextUniqueID")
  self.chk(rep)
  return rep.args[0].int64
 def ImageBitmapCreateX(self,arg_list):
  args=((ValueType.Address,c_uint64,getattr(arg_list,'value',arg_list)),)
  rep=self.sndrcv("ImageBitmapCreateX",*args)
  self.chk(rep)
  return (rep.status == tecrpc.Reply.Success)
 def ImageBitmapDestroy(self):
  rep=self.sndrcv("ImageBitmapDestroy")
  self.chk(rep)
 def ImageGetColorTable(self,red_array,green_array,blue_array):
  args=((ValueType.Array,c_uint8,red_array),
        (ValueType.Array,c_uint8,green_array),
        (ValueType.Array,c_uint8,blue_array),)
  rep=self.sndrcv("ImageGetColorTable",*args)
  self.chk(rep)
  memmove(red_array, rep.args[0].buffer, sizeof(red_array))
  memmove(green_array, rep.args[1].buffer, sizeof(green_array))
  memmove(blue_array, rep.args[2].buffer, sizeof(blue_array))
 def ImageGetDimensions(self):
  rep=self.sndrcv("ImageGetDimensions")
  self.chk(rep)
  return (
   (rep.status == tecrpc.Reply.Success),
   rep.args[0].int32,
   rep.args[1].int32)
 def ImageIndexedBitmapCreate(self,region,red_color_table_array,green_color_table_array,blue_color_table_array):
  args=((ValueType.Scalar,c_int32,ExportRegion(region).value),
        (ValueType.Array,c_uint8,red_color_table_array),
        (ValueType.Array,c_uint8,green_color_table_array),
        (ValueType.Array,c_uint8,blue_color_table_array),)
  rep=self.sndrcv("ImageIndexedBitmapCreate",*args)
  self.chk(rep)
  memmove(red_color_table_array, rep.args[0].buffer, sizeof(red_color_table_array))
  memmove(green_color_table_array, rep.args[1].buffer, sizeof(green_color_table_array))
  memmove(blue_color_table_array, rep.args[2].buffer, sizeof(blue_color_table_array))
  return (rep.status == tecrpc.Reply.Success)
 def ImageIndexedGetScanLine(self,scan_line,rgb_index_array):
  args=((ValueType.Scalar,c_int32,scan_line),
        (ValueType.Array,c_uint8,rgb_index_array),)
  rep=self.sndrcv("ImageIndexedGetScanLine",*args)
  self.chk(rep)
  memmove(rgb_index_array, rep.args[0].buffer, sizeof(rgb_index_array))
 def ImageRGBBitmapCreate(self,region):
  args=((ValueType.Scalar,c_int32,ExportRegion(region).value),)
  rep=self.sndrcv("ImageRGBBitmapCreate",*args)
  self.chk(rep)
  return (rep.status == tecrpc.Reply.Success)
 def ImageRGBGetScanLine(self,scan_line,red_array,green_array,blue_array):
  args=((ValueType.Scalar,c_int32,scan_line),
        (ValueType.Array,c_uint8,red_array),
        (ValueType.Array,c_uint8,green_array),
        (ValueType.Array,c_uint8,blue_array),)
  rep=self.sndrcv("ImageRGBGetScanLine",*args)
  self.chk(rep)
  memmove(red_array, rep.args[0].buffer, sizeof(red_array))
  memmove(green_array, rep.args[1].buffer, sizeof(green_array))
  memmove(blue_array, rep.args[2].buffer, sizeof(blue_array))
 def ImportAddConverter(self,converter_callback,converter_name,f_name_extension):
  args=((ValueType.Address,c_uint64,getattr(converter_callback,'value',converter_callback)),
        (ValueType.Text,None,converter_name),
        (ValueType.Text,None,f_name_extension),)
  rep=self.sndrcv("ImportAddConverter",*args)
  self.chk(rep)
  return (rep.status == tecrpc.Reply.Success)
 def ImportAddLoader(self,loader_callback,data_set_loader_name,loader_selected_callback,instruction_override_callback):
  args=((ValueType.Address,c_uint64,getattr(loader_callback,'value',loader_callback)),
        (ValueType.Text,None,data_set_loader_name),
        (ValueType.Address,c_uint64,getattr(loader_selected_callback,'value',loader_selected_callback)),
        (ValueType.Address,c_uint64,getattr(instruction_override_callback,'value',instruction_override_callback)),)
  rep=self.sndrcv("ImportAddLoader",*args)
  self.chk(rep)
  return (rep.status == tecrpc.Reply.Success)
 def ImportAddLoaderX(self,arg_list):
  args=((ValueType.Address,c_uint64,getattr(arg_list,'value',arg_list)),)
  rep=self.sndrcv("ImportAddLoaderX",*args)
  self.chk(rep)
  return (rep.status == tecrpc.Reply.Success)
 def ImportGetLoaderInstr(self):
  rep=self.sndrcv("ImportGetLoaderInstr")
  self.chk(rep)
  return (
   (rep.status == tecrpc.Reply.Success),
   self.read_text(rep.args[0]),
   rep.args[1].uint64)
 def ImportGetLoaderInstrByNum(self,index):
  args=((ValueType.Scalar,c_int32,index),)
  rep=self.sndrcv("ImportGetLoaderInstrByNum",*args)
  self.chk(rep)
  return (
   self.read_text(rep.args[0]),
   rep.args[1].uint64)
 def ImportGetLoaderInstrCount(self):
  rep=self.sndrcv("ImportGetLoaderInstrCount")
  self.chk(rep)
  return rep.args[0].int32
 def ImportResetLoaderInstr(self,data_set_loader_name,instructions):
  args=((ValueType.Text,None,data_set_loader_name),
        (ValueType.Address,c_uint64,getattr(instructions,'value',instructions)),)
  rep=self.sndrcv("ImportResetLoaderInstr",*args)
  self.chk(rep)
  return (rep.status == tecrpc.Reply.Success)
 def ImportSetLoaderInstr(self,data_set_loader_name,instructions):
  args=((ValueType.Text,None,data_set_loader_name),
        (ValueType.Address,c_uint64,getattr(instructions,'value',instructions)),)
  rep=self.sndrcv("ImportSetLoaderInstr",*args)
  self.chk(rep)
  return (rep.status == tecrpc.Reply.Success)
 def ImportWriteLoaderInstr(self,data_set_loader_name,instructions):
  args=((ValueType.Text,None,data_set_loader_name),
        (ValueType.Address,c_uint64,getattr(instructions,'value',instructions)),)
  rep=self.sndrcv("ImportWriteLoaderInstr",*args)
  self.chk(rep)
  return (rep.status == tecrpc.Reply.Success)
 def InterfaceGetBaseFontSize(self):
  rep=self.sndrcv("InterfaceGetBaseFontSize")
  self.chk(rep)
  return rep.args[0].int32
 def InterfaceGetDotsPerInch(self):
  rep=self.sndrcv("InterfaceGetDotsPerInch")
  self.chk(rep)
  return (
   rep.args[0].float64,
   rep.args[1].float64)
 def InterfaceSuspend(self,do_suspend):
  args=((ValueType.Scalar,c_bool,do_suspend),)
  rep=self.sndrcv("InterfaceSuspend",*args)
  self.chk(rep)
 def InterfaceWinAddPreMsgFn(self,pre_translate_message_proc):
  args=((ValueType.Address,c_uint64,getattr(pre_translate_message_proc,'value',pre_translate_message_proc)),)
  rep=self.sndrcv("InterfaceWinAddPreMsgFn",*args)
  self.chk(rep)
  return (rep.status == tecrpc.Reply.Success)
 def InternalDiagGetInfo(self,get_what):
  args=((ValueType.Scalar,c_int32,get_what),)
  rep=self.sndrcv("InternalDiagGetInfo",*args)
  self.chk(rep)
  return self.read_arbparam(rep.args[0])
 def InternalIsPrintDebugOn(self):
  rep=self.sndrcv("InternalIsPrintDebugOn")
  self.chk(rep)
  return (rep.status == tecrpc.Reply.Success)
 def Interrupt(self):
  rep=self.sndrcv("Interrupt")
  self.chk(rep)
 def InterruptCheck(self):
  rep=self.sndrcv("InterruptCheck")
  self.chk(rep)
  return rep.args[0].boolean
 def InterruptIsSet(self):
  rep=self.sndrcv("InterruptIsSet")
  self.chk(rep)
  return rep.args[0].boolean
 def InverseDistInterpolation(self,source_zones,dest_zone,var_list,inv_dist_exponent,inv_dist_min_radius,interp_pt_selection,interp_n_points):
  args=((ValueType.Address,c_uint64,getattr(source_zones,'value',source_zones)),
        (ValueType.Scalar,c_int32,dest_zone),
        (ValueType.Address,c_uint64,getattr(var_list,'value',var_list)),
        (ValueType.Scalar,c_double,inv_dist_exponent),
        (ValueType.Scalar,c_double,inv_dist_min_radius),
        (ValueType.Scalar,c_int32,PtSelection(interp_pt_selection).value),
        (ValueType.Scalar,c_int32,interp_n_points),)
  rep=self.sndrcv("InverseDistInterpolation",*args)
  self.chk(rep)
  return (rep.status == tecrpc.Reply.Success)
 def Krig(self,source_zones,dest_zone,var_list,krig_range,krig_zero_value,krig_drift,interp_pt_selection,interp_n_points):
  args=((ValueType.Address,c_uint64,getattr(source_zones,'value',source_zones)),
        (ValueType.Scalar,c_int32,dest_zone),
        (ValueType.Address,c_uint64,getattr(var_list,'value',var_list)),
        (ValueType.Scalar,c_double,krig_range),
        (ValueType.Scalar,c_double,krig_zero_value),
        (ValueType.Scalar,c_int32,Drift(krig_drift).value),
        (ValueType.Scalar,c_int32,PtSelection(interp_pt_selection).value),
        (ValueType.Scalar,c_int64,interp_n_points),)
  rep=self.sndrcv("Krig",*args)
  self.chk(rep)
  return (rep.status == tecrpc.Reply.Success)
 def LastErrorMessage(self):
  rep=self.sndrcv("LastErrorMessage")
  self.chk(rep)
  return self.read_text(rep.args[0])
 def LastErrorMessageClear(self):
  rep=self.sndrcv("LastErrorMessageClear")
  self.chk(rep)
 def LastErrorMessageType(self):
  rep=self.sndrcv("LastErrorMessageType")
  self.chk(rep)
  return try_cast_to_enum(MessageBoxType, rep.args[0].int32)
 def LimitGetValue(self,limit_string):
  args=((ValueType.Text,None,limit_string),)
  rep=self.sndrcv("LimitGetValue",*args)
  self.chk(rep)
  return rep.args[0].int64
 def LineMapCopy(self,source_map,dest_map):
  args=((ValueType.Scalar,c_int32,source_map),
        (ValueType.Scalar,c_int32,dest_map),)
  rep=self.sndrcv("LineMapCopy",*args)
  self.chk(rep)
  return (rep.status == tecrpc.Reply.Success)
 def LineMapCreate(self):
  rep=self.sndrcv("LineMapCreate")
  self.chk(rep)
  return (rep.status == tecrpc.Reply.Success)
 def LineMapDelete(self,maps_to_delete):
  args=((ValueType.Address,c_uint64,getattr(maps_to_delete,'value',maps_to_delete)),)
  rep=self.sndrcv("LineMapDelete",*args)
  self.chk(rep)
  return (rep.status == tecrpc.Reply.Success)
 def LineMapGetActive(self):
  rep=self.sndrcv("LineMapGetActive")
  self.chk(rep)
  return (
   (rep.status == tecrpc.Reply.Success),
   rep.args[0].uint64)
 def LineMapGetAssignment(self,line_map):
  args=((ValueType.Scalar,c_int32,line_map),)
  rep=self.sndrcv("LineMapGetAssignment",*args)
  self.chk(rep)
  return (
   rep.args[0].int32,
   rep.args[1].int32,
   rep.args[2].int32,
   rep.args[3].int32,
   rep.args[4].int32,
   try_cast_to_enum(FunctionDependency, rep.args[5].int32))
 def LineMapGetCount(self):
  rep=self.sndrcv("LineMapGetCount")
  self.chk(rep)
  return rep.args[0].int32
 def LineMapGetCountForFrame(self,frame_id):
  args=((ValueType.Scalar,c_int64,frame_id),)
  rep=self.sndrcv("LineMapGetCountForFrame",*args)
  self.chk(rep)
  return rep.args[0].int32
 def LineMapGetName(self,map):
  args=((ValueType.Scalar,c_int32,map),)
  rep=self.sndrcv("LineMapGetName",*args)
  self.chk(rep)
  return (
   (rep.status == tecrpc.Reply.Success),
   self.read_text(rep.args[0]))
 def LineMapGetNameForFrame(self,frame_id,map):
  args=((ValueType.Scalar,c_int64,frame_id),
        (ValueType.Scalar,c_int32,map),)
  rep=self.sndrcv("LineMapGetNameForFrame",*args)
  self.chk(rep)
  return (
   (rep.status == tecrpc.Reply.Success),
   self.read_text(rep.args[0]))
 def LineMapGetNumByUniqueID(self,unique_id):
  args=((ValueType.Scalar,c_int64,unique_id),)
  rep=self.sndrcv("LineMapGetNumByUniqueID",*args)
  self.chk(rep)
  return rep.args[0].int32
 def LineMapGetUniqueID(self,line_map):
  args=((ValueType.Scalar,c_int32,line_map),)
  rep=self.sndrcv("LineMapGetUniqueID",*args)
  self.chk(rep)
  return rep.args[0].int64
 def LineMapIsActive(self,line_map):
  args=((ValueType.Scalar,c_int32,line_map),)
  rep=self.sndrcv("LineMapIsActive",*args)
  self.chk(rep)
  return rep.args[0].boolean
 def LineMapIsActiveForFrame(self,frame_id,line_map):
  args=((ValueType.Scalar,c_int64,frame_id),
        (ValueType.Scalar,c_int32,line_map),)
  rep=self.sndrcv("LineMapIsActiveForFrame",*args)
  self.chk(rep)
  return rep.args[0].boolean
 def LineMapSetActive(self,line_map_set,assign_modifier):
  args=((ValueType.Address,c_uint64,getattr(line_map_set,'value',line_map_set)),
        (ValueType.Scalar,c_int32,AssignOp(assign_modifier).value),)
  rep=self.sndrcv("LineMapSetActive",*args)
  self.chk(rep)
  return try_cast_to_enum(SetValueReturnCode, rep.args[0].int32)
 def LineMapSetAssignment(self,attribute,line_map_set,d_value,i_value):
  args=((ValueType.Text,None,attribute),
        (ValueType.Address,c_uint64,getattr(line_map_set,'value',line_map_set)),
        (ValueType.Scalar,c_double,d_value),
        (ValueType.ArbParam,None,i_value),)
  rep=self.sndrcv("LineMapSetAssignment",*args)
  self.chk(rep)
  return try_cast_to_enum(SetValueReturnCode, rep.args[0].int32)
 def LineMapSetBarChart(self,attribute,line_map_set,d_value,i_value):
  args=((ValueType.Text,None,attribute),
        (ValueType.Address,c_uint64,getattr(line_map_set,'value',line_map_set)),
        (ValueType.Scalar,c_double,d_value),
        (ValueType.ArbParam,None,i_value),)
  rep=self.sndrcv("LineMapSetBarChart",*args)
  self.chk(rep)
  return try_cast_to_enum(SetValueReturnCode, rep.args[0].int32)
 def LineMapSetCurve(self,attribute,line_map_set,d_value,i_value):
  args=((ValueType.Text,None,attribute),
        (ValueType.Address,c_uint64,getattr(line_map_set,'value',line_map_set)),
        (ValueType.Scalar,c_double,d_value),
        (ValueType.ArbParam,None,i_value),)
  rep=self.sndrcv("LineMapSetCurve",*args)
  self.chk(rep)
  return try_cast_to_enum(SetValueReturnCode, rep.args[0].int32)
 def LineMapSetErrorBar(self,attribute,line_map_set,d_value,i_value):
  args=((ValueType.Text,None,attribute),
        (ValueType.Address,c_uint64,getattr(line_map_set,'value',line_map_set)),
        (ValueType.Scalar,c_double,d_value),
        (ValueType.ArbParam,None,i_value),)
  rep=self.sndrcv("LineMapSetErrorBar",*args)
  self.chk(rep)
  return try_cast_to_enum(SetValueReturnCode, rep.args[0].int32)
 def LineMapSetIndices(self,attribute,sub_attribute,line_map_set,i_value):
  args=((ValueType.Text,None,attribute),
        (ValueType.Text,None,sub_attribute),
        (ValueType.Address,c_uint64,getattr(line_map_set,'value',line_map_set)),
        (ValueType.ArbParam,None,i_value),)
  rep=self.sndrcv("LineMapSetIndices",*args)
  self.chk(rep)
  return try_cast_to_enum(SetValueReturnCode, rep.args[0].int32)
 def LineMapSetLine(self,attribute,line_map_set,d_value,i_value):
  args=((ValueType.Text,None,attribute),
        (ValueType.Address,c_uint64,getattr(line_map_set,'value',line_map_set)),
        (ValueType.Scalar,c_double,d_value),
        (ValueType.ArbParam,None,i_value),)
  rep=self.sndrcv("LineMapSetLine",*args)
  self.chk(rep)
  return try_cast_to_enum(SetValueReturnCode, rep.args[0].int32)
 def LineMapSetName(self,line_map_set,new_name):
  args=((ValueType.Address,c_uint64,getattr(line_map_set,'value',line_map_set)),
        (ValueType.Text,None,new_name),)
  rep=self.sndrcv("LineMapSetName",*args)
  self.chk(rep)
  return try_cast_to_enum(SetValueReturnCode, rep.args[0].int32)
 def LineMapSetSymbol(self,attribute,line_map_set,d_value,i_value):
  args=((ValueType.Text,None,attribute),
        (ValueType.Address,c_uint64,getattr(line_map_set,'value',line_map_set)),
        (ValueType.Scalar,c_double,d_value),
        (ValueType.ArbParam,None,i_value),)
  rep=self.sndrcv("LineMapSetSymbol",*args)
  self.chk(rep)
  return try_cast_to_enum(SetValueReturnCode, rep.args[0].int32)
 def LineMapSetSymbolShape(self,attribute,line_map_set,i_value):
  args=((ValueType.Text,None,attribute),
        (ValueType.Address,c_uint64,getattr(line_map_set,'value',line_map_set)),
        (ValueType.ArbParam,None,i_value),)
  rep=self.sndrcv("LineMapSetSymbolShape",*args)
  self.chk(rep)
  return try_cast_to_enum(SetValueReturnCode, rep.args[0].int32)
 def LineMapShiftToBottom(self,maps_to_shift):
  args=((ValueType.Address,c_uint64,getattr(maps_to_shift,'value',maps_to_shift)),)
  rep=self.sndrcv("LineMapShiftToBottom",*args)
  self.chk(rep)
  return (rep.status == tecrpc.Reply.Success)
 def LineMapShiftToTop(self,maps_to_shift):
  args=((ValueType.Address,c_uint64,getattr(maps_to_shift,'value',maps_to_shift)),)
  rep=self.sndrcv("LineMapShiftToTop",*args)
  self.chk(rep)
  return (rep.status == tecrpc.Reply.Success)
 def LineMapStyleGetArbValue(self,line_map,s1,s2,s3):
  args=((ValueType.Scalar,c_int32,line_map),
        (ValueType.Text,None,s1),
        (ValueType.Text,None,s2),
        (ValueType.Text,None,s3),)
  rep=self.sndrcv("LineMapStyleGetArbValue",*args)
  self.chk(rep)
  return self.read_arbparam(rep.args[0])
 def LineMapStyleGetArbValueForFrame(self,frame_id,line_map,s1,s2,s3):
  args=((ValueType.Scalar,c_int64,frame_id),
        (ValueType.Scalar,c_int32,line_map),
        (ValueType.Text,None,s1),
        (ValueType.Text,None,s2),
        (ValueType.Text,None,s3),)
  rep=self.sndrcv("LineMapStyleGetArbValueForFrame",*args)
  self.chk(rep)
  return self.read_arbparam(rep.args[0])
 def LineMapStyleGetDoubleValue(self,line_map,s1,s2,s3):
  args=((ValueType.Scalar,c_int32,line_map),
        (ValueType.Text,None,s1),
        (ValueType.Text,None,s2),
        (ValueType.Text,None,s3),)
  rep=self.sndrcv("LineMapStyleGetDoubleValue",*args)
  self.chk(rep)
  return rep.args[0].float64
 def LinePlotLayerIsActive(self,layer_show_flag):
  args=((ValueType.Text,None,layer_show_flag),)
  rep=self.sndrcv("LinePlotLayerIsActive",*args)
  self.chk(rep)
  return rep.args[0].boolean
 def LinePlotLayerIsActiveForFrame(self,frame_id,layer_show_flag):
  args=((ValueType.Scalar,c_int64,frame_id),
        (ValueType.Text,None,layer_show_flag),)
  rep=self.sndrcv("LinePlotLayerIsActiveForFrame",*args)
  self.chk(rep)
  return rep.args[0].boolean
 def LinePlotLayerSetIsActive(self,layer_show_flag,turn_on_line_plot_layer):
  args=((ValueType.Text,None,layer_show_flag),
        (ValueType.Scalar,c_bool,turn_on_line_plot_layer),)
  rep=self.sndrcv("LinePlotLayerSetIsActive",*args)
  self.chk(rep)
  return try_cast_to_enum(SetValueReturnCode, rep.args[0].int32)
 def LineSegProbe(self,line_seg_probe_result,starting_position,ending_positions,num_ending_positions,i_cell,j_cell,k_cell,cur_zone,zones_to_search,vars_to_return,line_seg_probe_callback,client_data):
  args=((ValueType.Address,c_uint64,getattr(line_seg_probe_result,'value',line_seg_probe_result)),
        (ValueType.Array,c_double,starting_position),
        (ValueType.Array,c_double,ending_positions),
        (ValueType.Scalar,c_int64,num_ending_positions),
        (ValueType.Scalar,c_int64,i_cell),
        (ValueType.Scalar,c_int64,j_cell),
        (ValueType.Scalar,c_int64,k_cell),
        (ValueType.Scalar,c_int32,cur_zone),
        (ValueType.Address,c_uint64,getattr(zones_to_search,'value',zones_to_search)),
        (ValueType.Address,c_uint64,getattr(vars_to_return,'value',vars_to_return)),
        (ValueType.Address,c_uint64,getattr(line_seg_probe_callback,'value',line_seg_probe_callback)),
        (ValueType.ArbParam,None,client_data),)
  rep=self.sndrcv("LineSegProbe",*args)
  self.chk(rep)
  return (rep.status == tecrpc.Reply.Success)
 def LineSegProbeGetFace(self,line_seg_probe_result,which_segment):
  args=((ValueType.Address,c_uint64,getattr(line_seg_probe_result,'value',line_seg_probe_result)),
        (ValueType.Scalar,c_int32,which_segment),)
  rep=self.sndrcv("LineSegProbeGetFace",*args)
  self.chk(rep)
  return rep.args[0].int32
 def LineSegProbeGetICell(self,line_seg_probe_result,which_segment):
  args=((ValueType.Address,c_uint64,getattr(line_seg_probe_result,'value',line_seg_probe_result)),
        (ValueType.Scalar,c_int32,which_segment),)
  rep=self.sndrcv("LineSegProbeGetICell",*args)
  self.chk(rep)
  return rep.args[0].int64
 def LineSegProbeGetJCell(self,line_seg_probe_result,which_segment):
  args=((ValueType.Address,c_uint64,getattr(line_seg_probe_result,'value',line_seg_probe_result)),
        (ValueType.Scalar,c_int32,which_segment),)
  rep=self.sndrcv("LineSegProbeGetJCell",*args)
  self.chk(rep)
  return rep.args[0].int64
 def LineSegProbeGetKCell(self,line_seg_probe_result,which_segment):
  args=((ValueType.Address,c_uint64,getattr(line_seg_probe_result,'value',line_seg_probe_result)),
        (ValueType.Scalar,c_int32,which_segment),)
  rep=self.sndrcv("LineSegProbeGetKCell",*args)
  self.chk(rep)
  return rep.args[0].int64
 def LineSegProbeGetStatus(self,line_seg_probe_result,which_segment):
  args=((ValueType.Address,c_uint64,getattr(line_seg_probe_result,'value',line_seg_probe_result)),
        (ValueType.Scalar,c_int32,which_segment),)
  rep=self.sndrcv("LineSegProbeGetStatus",*args)
  self.chk(rep)
  return try_cast_to_enum(ProbeStatus, rep.args[0].int32)
 def LineSegProbeGetVarValue(self,line_seg_probe_result,which_segment,var):
  args=((ValueType.Address,c_uint64,getattr(line_seg_probe_result,'value',line_seg_probe_result)),
        (ValueType.Scalar,c_int32,which_segment),
        (ValueType.Scalar,c_int32,var),)
  rep=self.sndrcv("LineSegProbeGetVarValue",*args)
  self.chk(rep)
  return rep.args[0].float64
 def LineSegProbeGetZone(self,line_seg_probe_result,which_segment):
  args=((ValueType.Address,c_uint64,getattr(line_seg_probe_result,'value',line_seg_probe_result)),
        (ValueType.Scalar,c_int32,which_segment),)
  rep=self.sndrcv("LineSegProbeGetZone",*args)
  self.chk(rep)
  return rep.args[0].int32
 def LineSegProbeResultAlloc(self):
  rep=self.sndrcv("LineSegProbeResultAlloc")
  self.chk(rep)
  return rep.args[0].uint64
 def LineSegProbeResultClear(self,line_seg_probe_result):
  args=((ValueType.Address,c_uint64,getattr(line_seg_probe_result,'value',line_seg_probe_result)),)
  rep=self.sndrcv("LineSegProbeResultClear",*args)
  self.chk(rep)
  return rep.args[0].uint64
 def LineSegProbeResultDealloc(self,line_seg_probe_result):
  args=((ValueType.Address,c_uint64,line_seg_probe_result.contents.value),)
  rep=self.sndrcv("LineSegProbeResultDealloc",*args)
  self.chk(rep)
  return rep.args[0].uint64
 def LineSegProbeResultGetCount(self,line_seg_probe_result):
  args=((ValueType.Address,c_uint64,getattr(line_seg_probe_result,'value',line_seg_probe_result)),)
  rep=self.sndrcv("LineSegProbeResultGetCount",*args)
  self.chk(rep)
  return rep.args[0].int32
 def LinearInterpolate(self,source_zones,dest_zone,var_list,linear_interp_const,linear_interp_mode):
  args=((ValueType.Address,c_uint64,getattr(source_zones,'value',source_zones)),
        (ValueType.Scalar,c_int32,dest_zone),
        (ValueType.Address,c_uint64,getattr(var_list,'value',var_list)),
        (ValueType.Scalar,c_double,linear_interp_const),
        (ValueType.Scalar,c_int32,LinearInterpMode(linear_interp_mode).value),)
  rep=self.sndrcv("LinearInterpolate",*args)
  self.chk(rep)
  return (rep.status == tecrpc.Reply.Success)
 def LinkingGetValue(self,attribute,sub_attribute):
  args=((ValueType.Text,None,attribute),
        (ValueType.Text,None,sub_attribute),)
  rep=self.sndrcv("LinkingGetValue",*args)
  self.chk(rep)
  return self.read_arbparam(rep.args[0])
 def LinkingSetValue(self,attribute,sub_attribute,i_value):
  args=((ValueType.Text,None,attribute),
        (ValueType.Text,None,sub_attribute),
        (ValueType.ArbParam,None,i_value),)
  rep=self.sndrcv("LinkingSetValue",*args)
  self.chk(rep)
  return try_cast_to_enum(SetValueReturnCode, rep.args[0].int32)
 def LockFinish(self,add_on):
  args=((ValueType.Address,c_uint64,getattr(add_on,'value',add_on)),)
  rep=self.sndrcv("LockFinish",*args)
  self.chk(rep)
 def LockGetCount(self):
  rep=self.sndrcv("LockGetCount")
  self.chk(rep)
  return rep.args[0].int32
 def LockGetCurrentOwnerName(self):
  rep=self.sndrcv("LockGetCurrentOwnerName")
  self.chk(rep)
  return self.read_text(rep.args[0])
 def LockIsOn(self):
  rep=self.sndrcv("LockIsOn")
  self.chk(rep)
  return rep.args[0].boolean
 def LockOff(self):
  rep=self.sndrcv("LockOff")
  self.chk(rep)
 def LockOn(self):
  rep=self.sndrcv("LockOn")
  self.chk(rep)
 def LockStart(self,add_on):
  args=((ValueType.Address,c_uint64,getattr(add_on,'value',add_on)),)
  rep=self.sndrcv("LockStart",*args)
  self.chk(rep)
 def MacroAddCommandCallback(self,command_processor_id_string,macro_command_callback):
  args=((ValueType.Text,None,command_processor_id_string),
        (ValueType.Address,c_uint64,getattr(macro_command_callback,'value',macro_command_callback)),)
  rep=self.sndrcv("MacroAddCommandCallback",*args)
  self.chk(rep)
  return (rep.status == tecrpc.Reply.Success)
 def MacroExecuteCommand(self,command):
  args=((ValueType.Text,None,command),)
  rep=self.sndrcv("MacroExecuteCommand",*args)
  self.chk(rep)
  return (rep.status == tecrpc.Reply.Success)
 def MacroExecuteExtendedCommand(self,command_processor_id,command,raw_data):
  args=((ValueType.Text,None,command_processor_id),
        (ValueType.Text,None,command),
        (ValueType.Text,None,raw_data),)
  rep=self.sndrcv("MacroExecuteExtendedCommand",*args)
  self.chk(rep)
  return (rep.status == tecrpc.Reply.Success)
 def MacroFunctionExists(self,function_name):
  args=((ValueType.Text,None,function_name),)
  rep=self.sndrcv("MacroFunctionExists",*args)
  self.chk(rep)
  return (rep.status == tecrpc.Reply.Success)
 def MacroFunctionGetAcceleratorKey(self,index):
  args=((ValueType.Scalar,c_int32,index),)
  rep=self.sndrcv("MacroFunctionGetAcceleratorKey",*args)
  self.chk(rep)
  return rep.args[0].text[0]
 def MacroFunctionGetCount(self):
  rep=self.sndrcv("MacroFunctionGetCount")
  self.chk(rep)
  return rep.args[0].int32
 def MacroFunctionGetName(self,index):
  args=((ValueType.Scalar,c_int32,index),)
  rep=self.sndrcv("MacroFunctionGetName",*args)
  self.chk(rep)
  return (
   (rep.status == tecrpc.Reply.Success),
   self.read_text(rep.args[0]))
 def MacroGetDebugger(self):
  rep=self.sndrcv("MacroGetDebugger")
  self.chk(rep)
  return self.rep.args[0].uint64
 def MacroIsBatchModeActive(self):
  rep=self.sndrcv("MacroIsBatchModeActive")
  self.chk(rep)
  return rep.args[0].boolean
 def MacroIsRecordingActive(self):
  rep=self.sndrcv("MacroIsRecordingActive")
  self.chk(rep)
  return rep.args[0].boolean
 def MacroRecordExtComRaw(self,command_processor_id_string,command,raw_data):
  args=((ValueType.Text,None,command_processor_id_string),
        (ValueType.Text,None,command),
        (ValueType.Text,None,raw_data),)
  rep=self.sndrcv("MacroRecordExtComRaw",*args)
  self.chk(rep)
  return (rep.status == tecrpc.Reply.Success)
 def MacroRecordExtCommand(self,command_processor_id_string,command):
  args=((ValueType.Text,None,command_processor_id_string),
        (ValueType.Text,None,command),)
  rep=self.sndrcv("MacroRecordExtCommand",*args)
  self.chk(rep)
  return (rep.status == tecrpc.Reply.Success)
 def MacroRecordRawCommand(self,command):
  args=((ValueType.Text,None,command),)
  rep=self.sndrcv("MacroRecordRawCommand",*args)
  self.chk(rep)
  return (rep.status == tecrpc.Reply.Success)
 def MacroRunFile(self,f_name):
  args=((ValueType.Text,None,f_name),)
  rep=self.sndrcv("MacroRunFile",*args)
  self.chk(rep)
  return (rep.status == tecrpc.Reply.Success)
 def MacroRunFunction(self,quick_macro_name,macro_parameters):
  args=((ValueType.Text,None,quick_macro_name),
        (ValueType.Text,None,macro_parameters),)
  rep=self.sndrcv("MacroRunFunction",*args)
  self.chk(rep)
  return (rep.status == tecrpc.Reply.Success)
 def MacroSetMacroVar(self,macro_var,value_string):
  args=((ValueType.Text,None,macro_var),
        (ValueType.Text,None,value_string),)
  rep=self.sndrcv("MacroSetMacroVar",*args)
  self.chk(rep)
  return (rep.status == tecrpc.Reply.Success)
 def MainlineInvoke(self,job,job_data):
  args=((ValueType.Address,c_uint64,getattr(job,'value',job)),
        (ValueType.ArbParam,None,job_data),)
  rep=self.sndrcv("MainlineInvoke",*args)
  self.chk(rep)
 def MenuActivate(self,activate):
  args=((ValueType.Scalar,c_bool,activate),)
  rep=self.sndrcv("MenuActivate",*args)
  self.chk(rep)
 def MenuAddStatusLineHelp(self,menu_item,status_line_help):
  args=((ValueType.Address,c_uint64,getattr(menu_item,'value',menu_item)),
        (ValueType.Text,None,status_line_help),)
  rep=self.sndrcv("MenuAddStatusLineHelp",*args)
  self.chk(rep)
 def MenuClearAll(self):
  rep=self.sndrcv("MenuClearAll")
  self.chk(rep)
 def MenuDelete(self,menu_item_ptr):
  args=((ValueType.Address,c_uint64,menu_item_ptr.contents.value),)
  rep=self.sndrcv("MenuDelete",*args)
  self.chk(rep)
  return rep.args[0].uint64
 def MenuGetMain(self):
  rep=self.sndrcv("MenuGetMain")
  self.chk(rep)
  return rep.args[0].uint64
 def MenuGetStandard(self,standard_menu):
  args=((ValueType.Scalar,c_int32,StandardMenu(standard_menu).value),)
  rep=self.sndrcv("MenuGetStandard",*args)
  self.chk(rep)
  return rep.args[0].uint64
 def MenuInsertSeparator(self,parent_menu,insert_pos):
  args=((ValueType.Address,c_uint64,getattr(parent_menu,'value',parent_menu)),
        (ValueType.Scalar,c_int32,insert_pos),)
  rep=self.sndrcv("MenuInsertSeparator",*args)
  self.chk(rep)
  return rep.args[0].uint64
 def MenuInsertStandard(self,parent_menu,insert_pos,standard_menu):
  args=((ValueType.Address,c_uint64,getattr(parent_menu,'value',parent_menu)),
        (ValueType.Scalar,c_int32,insert_pos),
        (ValueType.Scalar,c_int32,StandardMenu(standard_menu).value),)
  rep=self.sndrcv("MenuInsertStandard",*args)
  self.chk(rep)
 def MenuInsertSubMenu(self,parent_menu,insert_pos,sub_menu_label):
  args=((ValueType.Address,c_uint64,getattr(parent_menu,'value',parent_menu)),
        (ValueType.Scalar,c_int32,insert_pos),
        (ValueType.Text,None,sub_menu_label),)
  rep=self.sndrcv("MenuInsertSubMenu",*args)
  self.chk(rep)
  return rep.args[0].uint64
 def MenuInsertToggle(self,parent_menu,insert_pos,toggle_label,activate_callback,activate_client_data,get_toggle_state_callback,get_toggle_state_client_data):
  args=((ValueType.Address,c_uint64,getattr(parent_menu,'value',parent_menu)),
        (ValueType.Scalar,c_int32,insert_pos),
        (ValueType.Text,None,toggle_label),
        (ValueType.Address,c_uint64,getattr(activate_callback,'value',activate_callback)),
        (ValueType.ArbParam,None,activate_client_data),
        (ValueType.Address,c_uint64,getattr(get_toggle_state_callback,'value',get_toggle_state_callback)),
        (ValueType.ArbParam,None,get_toggle_state_client_data),)
  rep=self.sndrcv("MenuInsertToggle",*args)
  self.chk(rep)
  return rep.args[0].uint64
 def MenuRegisterSensitivityCallback(self,menu_item,get_sensitivity_callback,get_sensitivity_client_data):
  args=((ValueType.Address,c_uint64,getattr(menu_item,'value',menu_item)),
        (ValueType.Address,c_uint64,getattr(get_sensitivity_callback,'value',get_sensitivity_callback)),
        (ValueType.ArbParam,None,get_sensitivity_client_data),)
  rep=self.sndrcv("MenuRegisterSensitivityCallback",*args)
  self.chk(rep)
 def MouseGetCurrentMode(self):
  rep=self.sndrcv("MouseGetCurrentMode")
  self.chk(rep)
  return try_cast_to_enum(MouseButtonMode, rep.args[0].int32)
 def MouseIsValidMode(self,mouse_mode):
  args=((ValueType.Scalar,c_int32,MouseButtonMode(mouse_mode).value),)
  rep=self.sndrcv("MouseIsValidMode",*args)
  self.chk(rep)
  return rep.args[0].boolean
 def MouseSetMode(self,mouse_mode):
  args=((ValueType.Scalar,c_int32,MouseButtonMode(mouse_mode).value),)
  rep=self.sndrcv("MouseSetMode",*args)
  self.chk(rep)
  return (rep.status == tecrpc.Reply.Success)
 def NewLayout(self):
  rep=self.sndrcv("NewLayout")
  self.chk(rep)
  return (rep.status == tecrpc.Reply.Success)
 def OnIdleQueueAddCallback(self,callback,client_data):
  args=((ValueType.Address,c_uint64,getattr(callback,'value',callback)),
        (ValueType.ArbParam,None,client_data),)
  rep=self.sndrcv("OnIdleQueueAddCallback",*args)
  self.chk(rep)
  return (rep.status == tecrpc.Reply.Success)
 def OnIdleQueueRemoveCallback(self,callback,client_data):
  args=((ValueType.Address,c_uint64,getattr(callback,'value',callback)),
        (ValueType.ArbParam,None,client_data),)
  rep=self.sndrcv("OnIdleQueueRemoveCallback",*args)
  self.chk(rep)
  return (rep.status == tecrpc.Reply.Success)
 def OpenLayout(self,f_name,alt_instructions,append):
  args=((ValueType.Text,None,f_name),
        (ValueType.Address,c_uint64,getattr(alt_instructions,'value',alt_instructions)),
        (ValueType.Scalar,c_bool,append),)
  rep=self.sndrcv("OpenLayout",*args)
  self.chk(rep)
  return (rep.status == tecrpc.Reply.Success)
 def OpenLayoutX(self,arg_list):
  args=((ValueType.Address,c_uint64,getattr(arg_list,'value',arg_list)),)
  rep=self.sndrcv("OpenLayoutX",*args)
  self.chk(rep)
  return (rep.status == tecrpc.Reply.Success)
 def PageClear(self):
  rep=self.sndrcv("PageClear")
  self.chk(rep)
 def PageCreateNew(self):
  rep=self.sndrcv("PageCreateNew")
  self.chk(rep)
  return (rep.status == tecrpc.Reply.Success)
 def PageDelete(self):
  rep=self.sndrcv("PageDelete")
  self.chk(rep)
 def PageGetCount(self):
  rep=self.sndrcv("PageGetCount")
  self.chk(rep)
  return rep.args[0].int32
 def PageGetName(self):
  rep=self.sndrcv("PageGetName")
  self.chk(rep)
  return (
   (rep.status == tecrpc.Reply.Success),
   self.read_text(rep.args[0]))
 def PageGetPosByUniqueID(self,unique_id):
  args=((ValueType.Scalar,c_int64,unique_id),)
  rep=self.sndrcv("PageGetPosByUniqueID",*args)
  self.chk(rep)
  return rep.args[0].int32
 def PageGetUniqueID(self):
  rep=self.sndrcv("PageGetUniqueID")
  self.chk(rep)
  return rep.args[0].int64
 def PageSetCurrentByName(self,page_name):
  args=((ValueType.Text,None,page_name),)
  rep=self.sndrcv("PageSetCurrentByName",*args)
  self.chk(rep)
  return (rep.status == tecrpc.Reply.Success)
 def PageSetCurrentByUniqueID(self,unique_id):
  args=((ValueType.Scalar,c_int64,unique_id),)
  rep=self.sndrcv("PageSetCurrentByUniqueID",*args)
  self.chk(rep)
  return (rep.status == tecrpc.Reply.Success)
 def PageSetCurrentToNext(self):
  rep=self.sndrcv("PageSetCurrentToNext")
  self.chk(rep)
 def PageSetCurrentToPrev(self):
  rep=self.sndrcv("PageSetCurrentToPrev")
  self.chk(rep)
 def PageSetName(self,name):
  args=((ValueType.Text,None,name),)
  rep=self.sndrcv("PageSetName",*args)
  self.chk(rep)
  return try_cast_to_enum(SetValueReturnCode, rep.args[0].int32)
 def PaperGetDimensions(self):
  rep=self.sndrcv("PaperGetDimensions")
  self.chk(rep)
  return (
   rep.args[0].float64,
   rep.args[1].float64)
 def ParentLockFinish(self):
  rep=self.sndrcv("ParentLockFinish")
  self.chk(rep)
 def ParentLockStart(self,shutdown_implicit_recording):
  args=((ValueType.Scalar,c_bool,shutdown_implicit_recording),)
  rep=self.sndrcv("ParentLockStart",*args)
  self.chk(rep)
 def PickAddAll(self,object_type):
  args=((ValueType.Scalar,c_int32,PickObjects(object_type).value),)
  rep=self.sndrcv("PickAddAll",*args)
  self.chk(rep)
  return (rep.status == tecrpc.Reply.Success)
 def PickAddAllInRectX(self,arg_list):
  args=((ValueType.Address,c_uint64,getattr(arg_list,'value',arg_list)),)
  rep=self.sndrcv("PickAddAllInRectX",*args)
  self.chk(rep)
  return (rep.status == tecrpc.Reply.Success)
 def PickAddAtPositionX(self,arg_list):
  args=((ValueType.Address,c_uint64,getattr(arg_list,'value',arg_list)),)
  rep=self.sndrcv("PickAddAtPositionX",*args)
  self.chk(rep)
  return (rep.status == tecrpc.Reply.Success)
 def PickAddFrameByUniqueID(self,collecting_objects,unique_id):
  args=((ValueType.Scalar,c_bool,collecting_objects),
        (ValueType.Scalar,c_int64,unique_id),)
  rep=self.sndrcv("PickAddFrameByUniqueID",*args)
  self.chk(rep)
  return (rep.status == tecrpc.Reply.Success)
 def PickAddLineMaps(self,collecting_objects,line_map_set):
  args=((ValueType.Scalar,c_bool,collecting_objects),
        (ValueType.Address,c_uint64,getattr(line_map_set,'value',line_map_set)),)
  rep=self.sndrcv("PickAddLineMaps",*args)
  self.chk(rep)
  return (rep.status == tecrpc.Reply.Success)
 def PickAddZones(self,collecting_objects,zone_set):
  args=((ValueType.Scalar,c_bool,collecting_objects),
        (ValueType.Address,c_uint64,getattr(zone_set,'value',zone_set)),)
  rep=self.sndrcv("PickAddZones",*args)
  self.chk(rep)
  return (rep.status == tecrpc.Reply.Success)
 def PickClear(self):
  rep=self.sndrcv("PickClear")
  self.chk(rep)
  return (rep.status == tecrpc.Reply.Success)
 def PickCopy(self):
  rep=self.sndrcv("PickCopy")
  self.chk(rep)
  return (rep.status == tecrpc.Reply.Success)
 def PickCut(self):
  rep=self.sndrcv("PickCut")
  self.chk(rep)
  return (rep.status == tecrpc.Reply.Success)
 def PickDeselect(self,pick_list_item):
  args=((ValueType.Scalar,c_int32,pick_list_item),)
  rep=self.sndrcv("PickDeselect",*args)
  self.chk(rep)
  return (rep.status == tecrpc.Reply.Success)
 def PickDeselectAll(self):
  rep=self.sndrcv("PickDeselectAll")
  self.chk(rep)
  return (rep.status == tecrpc.Reply.Success)
 def PickEdit(self,action):
  args=((ValueType.Text,None,action),)
  rep=self.sndrcv("PickEdit",*args)
  self.chk(rep)
  return (rep.status == tecrpc.Reply.Success)
 def PickEditLowLevel(self,d_value,i_value,p1,p2):
  args=((ValueType.Scalar,c_double,d_value),
        (ValueType.ArbParam,None,i_value),
        (ValueType.Text,None,p1),
        (ValueType.Text,None,p2),)
  rep=self.sndrcv("PickEditLowLevel",*args)
  self.chk(rep)
  return (rep.status == tecrpc.Reply.Success)
 def PickGeom(self,gid):
  args=((ValueType.Scalar,c_int64,gid),)
  rep=self.sndrcv("PickGeom",*args)
  self.chk(rep)
  return (rep.status == tecrpc.Reply.Success)
 def PickIsSnapToGridAllowed(self):
  rep=self.sndrcv("PickIsSnapToGridAllowed")
  self.chk(rep)
  return rep.args[0].boolean
 def PickIsSnapToPaperAllowed(self):
  rep=self.sndrcv("PickIsSnapToPaperAllowed")
  self.chk(rep)
  return rep.args[0].boolean
 def PickListGetAxisKind(self,pick_list_index):
  args=((ValueType.Scalar,c_int32,pick_list_index),)
  rep=self.sndrcv("PickListGetAxisKind",*args)
  self.chk(rep)
  return rep.args[0].text[0]
 def PickListGetAxisNumber(self,pick_list_index):
  args=((ValueType.Scalar,c_int32,pick_list_index),)
  rep=self.sndrcv("PickListGetAxisNumber",*args)
  self.chk(rep)
  return rep.args[0].int32
 def PickListGetAxisSubObject(self,pick_list_index):
  args=((ValueType.Scalar,c_int32,pick_list_index),)
  rep=self.sndrcv("PickListGetAxisSubObject",*args)
  self.chk(rep)
  return try_cast_to_enum(AxisSubObject, rep.args[0].int32)
 def PickListGetCount(self):
  rep=self.sndrcv("PickListGetCount")
  self.chk(rep)
  return rep.args[0].int32
 def PickListGetFrameName(self,pick_list_index):
  args=((ValueType.Scalar,c_int32,pick_list_index),)
  rep=self.sndrcv("PickListGetFrameName",*args)
  self.chk(rep)
  return self.read_text(rep.args[0])
 def PickListGetFrameUniqueID(self,pick_list_index):
  args=((ValueType.Scalar,c_int32,pick_list_index),)
  rep=self.sndrcv("PickListGetFrameUniqueID",*args)
  self.chk(rep)
  return rep.args[0].int64
 def PickListGetGeom(self,pick_list_index):
  args=((ValueType.Scalar,c_int32,pick_list_index),)
  rep=self.sndrcv("PickListGetGeom",*args)
  self.chk(rep)
  return rep.args[0].int64
 def PickListGetGeomInfo(self,pick_list_index):
  args=((ValueType.Scalar,c_int32,pick_list_index),)
  rep=self.sndrcv("PickListGetGeomInfo",*args)
  self.chk(rep)
  return (
   rep.args[0].int32,
   rep.args[1].int64)
 def PickListGetIsoSurfaceGroup(self,pick_list_index):
  args=((ValueType.Scalar,c_int32,pick_list_index),)
  rep=self.sndrcv("PickListGetIsoSurfaceGroup",*args)
  self.chk(rep)
  return rep.args[0].int32
 def PickListGetLabelsContourGroup(self,pick_list_index):
  args=((ValueType.Scalar,c_int32,pick_list_index),)
  rep=self.sndrcv("PickListGetLabelsContourGroup",*args)
  self.chk(rep)
  return rep.args[0].int32
 def PickListGetLegendContourGroup(self,pick_list_index):
  args=((ValueType.Scalar,c_int32,pick_list_index),)
  rep=self.sndrcv("PickListGetLegendContourGroup",*args)
  self.chk(rep)
  return rep.args[0].int32
 def PickListGetLineMapIndex(self,pick_list_index):
  args=((ValueType.Scalar,c_int32,pick_list_index),)
  rep=self.sndrcv("PickListGetLineMapIndex",*args)
  self.chk(rep)
  return rep.args[0].int64
 def PickListGetLineMapNumber(self,pick_list_index):
  args=((ValueType.Scalar,c_int32,pick_list_index),)
  rep=self.sndrcv("PickListGetLineMapNumber",*args)
  self.chk(rep)
  return rep.args[0].int32
 def PickListGetSliceGroup(self,pick_list_index):
  args=((ValueType.Scalar,c_int32,pick_list_index),)
  rep=self.sndrcv("PickListGetSliceGroup",*args)
  self.chk(rep)
  return rep.args[0].int32
 def PickListGetText(self,pick_list_index):
  args=((ValueType.Scalar,c_int32,pick_list_index),)
  rep=self.sndrcv("PickListGetText",*args)
  self.chk(rep)
  return rep.args[0].int64
 def PickListGetType(self,pick_list_index):
  args=((ValueType.Scalar,c_int32,pick_list_index),)
  rep=self.sndrcv("PickListGetType",*args)
  self.chk(rep)
  return try_cast_to_enum(PickObjects, rep.args[0].int32)
 def PickListGetZoneIndices(self,pick_list_index):
  args=((ValueType.Scalar,c_int32,pick_list_index),)
  rep=self.sndrcv("PickListGetZoneIndices",*args)
  self.chk(rep)
  return (
   rep.args[0].int64,
   rep.args[1].int64,
   rep.args[2].int64)
 def PickListGetZoneNumber(self,pick_list_index):
  args=((ValueType.Scalar,c_int32,pick_list_index),)
  rep=self.sndrcv("PickListGetZoneNumber",*args)
  self.chk(rep)
  return rep.args[0].int32
 def PickMagnify(self,mag_factor):
  args=((ValueType.Scalar,c_double,mag_factor),)
  rep=self.sndrcv("PickMagnify",*args)
  self.chk(rep)
  return (rep.status == tecrpc.Reply.Success)
 def PickPaste(self):
  rep=self.sndrcv("PickPaste")
  self.chk(rep)
  return (rep.status == tecrpc.Reply.Success)
 def PickPop(self):
  rep=self.sndrcv("PickPop")
  self.chk(rep)
  return (rep.status == tecrpc.Reply.Success)
 def PickPush(self):
  rep=self.sndrcv("PickPush")
  self.chk(rep)
  return (rep.status == tecrpc.Reply.Success)
 def PickShift(self,dx_paper,dy_paper,pointer_style):
  args=((ValueType.Scalar,c_double,dx_paper),
        (ValueType.Scalar,c_double,dy_paper),
        (ValueType.Scalar,c_int32,PointerStyle(pointer_style).value),)
  rep=self.sndrcv("PickShift",*args)
  self.chk(rep)
  return (rep.status == tecrpc.Reply.Success)
 def PickText(self,tid):
  args=((ValueType.Scalar,c_int64,tid),)
  rep=self.sndrcv("PickText",*args)
  self.chk(rep)
  return (rep.status == tecrpc.Reply.Success)
 def PleaseWait(self,wait_message,do_wait):
  args=((ValueType.Text,None,wait_message),
        (ValueType.Scalar,c_bool,do_wait),)
  rep=self.sndrcv("PleaseWait",*args)
  self.chk(rep)
 def PopMainProcessWindow(self):
  rep=self.sndrcv("PopMainProcessWindow")
  self.chk(rep)
 def PostLastErrorMessage(self):
  rep=self.sndrcv("PostLastErrorMessage")
  self.chk(rep)
 def Print(self):
  rep=self.sndrcv("Print")
  self.chk(rep)
  return (rep.status == tecrpc.Reply.Success)
 def PrintSetup(self,attribute,sub_attribute,d_value,i_value):
  args=((ValueType.Text,None,attribute),
        (ValueType.Text,None,sub_attribute),
        (ValueType.Scalar,c_double,d_value),
        (ValueType.ArbParam,None,i_value),)
  rep=self.sndrcv("PrintSetup",*args)
  self.chk(rep)
  return try_cast_to_enum(SetValueReturnCode, rep.args[0].int32)
 def ProbeAllowCOBs(self):
  rep=self.sndrcv("ProbeAllowCOBs")
  self.chk(rep)
 def ProbeAtFieldIndexX(self,arg_list):
  args=((ValueType.Address,c_uint64,getattr(arg_list,'value',arg_list)),)
  rep=self.sndrcv("ProbeAtFieldIndexX",*args)
  self.chk(rep)
 def ProbeAtFieldPositionX(self,arg_list):
  args=((ValueType.Address,c_uint64,getattr(arg_list,'value',arg_list)),)
  rep=self.sndrcv("ProbeAtFieldPositionX",*args)
  self.chk(rep)
 def ProbeAtLineIndexX(self,arg_list):
  args=((ValueType.Address,c_uint64,getattr(arg_list,'value',arg_list)),)
  rep=self.sndrcv("ProbeAtLineIndexX",*args)
  self.chk(rep)
 def ProbeAtLinePositionX(self,arg_list):
  args=((ValueType.Address,c_uint64,getattr(arg_list,'value',arg_list)),)
  rep=self.sndrcv("ProbeAtLinePositionX",*args)
  self.chk(rep)
 def ProbeAtPosSequenceBeginX(self,arg_list):
  args=((ValueType.Address,c_uint64,getattr(arg_list,'value',arg_list)),)
  rep=self.sndrcv("ProbeAtPosSequenceBeginX",*args)
  self.chk(rep)
 def ProbeAtPosSequenceEnd(self):
  rep=self.sndrcv("ProbeAtPosSequenceEnd")
  self.chk(rep)
 def ProbeAtPosition(self,x,y,z,i_cell,j_cell,k_cell,plane,cur_zone,start_with_local_cell,v_value_array,source_zones,search_volume,get_zone_only,get_nearest_point):
  args=((ValueType.Scalar,c_double,x),
        (ValueType.Scalar,c_double,y),
        (ValueType.Scalar,c_double,z),
        (ValueType.Scalar,c_int64,i_cell),
        (ValueType.Scalar,c_int64,j_cell),
        (ValueType.Scalar,c_int64,k_cell),
        (ValueType.Scalar,c_int32,IJKPlanes(plane).value),
        (ValueType.Scalar,c_int32,cur_zone),
        (ValueType.Scalar,c_bool,start_with_local_cell),
        (ValueType.Array,c_double,v_value_array),
        (ValueType.Address,c_uint64,getattr(source_zones,'value',source_zones)),
        (ValueType.Scalar,c_bool,search_volume),
        (ValueType.Scalar,c_bool,get_zone_only),
        (ValueType.Scalar,c_bool,get_nearest_point),)
  rep=self.sndrcv("ProbeAtPosition",*args)
  self.chk(rep)
  memmove(v_value_array, rep.args[5].buffer, sizeof(v_value_array))
  return (
   (rep.status == tecrpc.Reply.Success),
   rep.args[0].int64,
   rep.args[1].int64,
   rep.args[2].int64,
   try_cast_to_enum(IJKPlanes, rep.args[3].int32),
   rep.args[4].int32)
 def ProbeFieldGetCCValue(self,var):
  args=((ValueType.Scalar,c_int32,var),)
  rep=self.sndrcv("ProbeFieldGetCCValue",*args)
  self.chk(rep)
  return (
   (rep.status == tecrpc.Reply.Success),
   rep.args[0].float64)
 def ProbeFieldGetCZType(self):
  rep=self.sndrcv("ProbeFieldGetCZType")
  self.chk(rep)
  return try_cast_to_enum(CZType, rep.args[0].int32)
 def ProbeFieldGetCell(self):
  rep=self.sndrcv("ProbeFieldGetCell")
  self.chk(rep)
  return rep.args[0].int64
 def ProbeFieldGetFaceCell(self):
  rep=self.sndrcv("ProbeFieldGetFaceCell")
  self.chk(rep)
  return rep.args[0].int64
 def ProbeFieldGetFaceNumber(self):
  rep=self.sndrcv("ProbeFieldGetFaceNumber")
  self.chk(rep)
  return rep.args[0].int32
 def ProbeFieldGetName(self):
  rep=self.sndrcv("ProbeFieldGetName")
  self.chk(rep)
  return (
   (rep.status == tecrpc.Reply.Success),
   self.read_text(rep.args[0]))
 def ProbeFieldGetNativeRef(self,var):
  args=((ValueType.Scalar,c_int32,var),)
  rep=self.sndrcv("ProbeFieldGetNativeRef",*args)
  self.chk(rep)
  return rep.args[0].uint64
 def ProbeFieldGetPlane(self):
  rep=self.sndrcv("ProbeFieldGetPlane")
  self.chk(rep)
  return try_cast_to_enum(IJKPlanes, rep.args[0].int32)
 def ProbeFieldGetReadableCCRef(self,var):
  args=((ValueType.Scalar,c_int32,var),)
  rep=self.sndrcv("ProbeFieldGetReadableCCRef",*args)
  self.chk(rep)
  return rep.args[0].uint64
 def ProbeFieldGetReadableDerivedRef(self,var):
  args=((ValueType.Scalar,c_int32,var),)
  rep=self.sndrcv("ProbeFieldGetReadableDerivedRef",*args)
  self.chk(rep)
  return rep.args[0].uint64
 def ProbeFieldGetReadableNLRef(self,var):
  args=((ValueType.Scalar,c_int32,var),)
  rep=self.sndrcv("ProbeFieldGetReadableNLRef",*args)
  self.chk(rep)
  return rep.args[0].uint64
 def ProbeFieldGetReadableNativeRef(self,var):
  args=((ValueType.Scalar,c_int32,var),)
  rep=self.sndrcv("ProbeFieldGetReadableNativeRef",*args)
  self.chk(rep)
  return rep.args[0].uint64
 def ProbeFieldGetValue(self,var):
  args=((ValueType.Scalar,c_int32,var),)
  rep=self.sndrcv("ProbeFieldGetValue",*args)
  self.chk(rep)
  return rep.args[0].float64
 def ProbeFieldGetZone(self):
  rep=self.sndrcv("ProbeFieldGetZone")
  self.chk(rep)
  return rep.args[0].int32
 def ProbeFieldIsVarValid(self,var):
  args=((ValueType.Scalar,c_int32,var),)
  rep=self.sndrcv("ProbeFieldIsVarValid",*args)
  self.chk(rep)
  return rep.args[0].boolean
 def ProbeGetPlotType(self):
  rep=self.sndrcv("ProbeGetPlotType")
  self.chk(rep)
  return try_cast_to_enum(PlotType, rep.args[0].int32)
 def ProbeGetPointIndex(self):
  rep=self.sndrcv("ProbeGetPointIndex")
  self.chk(rep)
  return rep.args[0].int64
 def ProbeInfoDealloc(self,probe_info):
  args=((ValueType.Address,c_uint64,probe_info.contents.value),)
  rep=self.sndrcv("ProbeInfoDealloc",*args)
  self.chk(rep)
  return rep.args[0].uint64
 def ProbeInfoGet(self):
  rep=self.sndrcv("ProbeInfoGet")
  self.chk(rep)
  return rep.args[0].uint64
 def ProbeInstallCallback(self,probe_destination,information_line_text):
  args=((ValueType.Address,c_uint64,getattr(probe_destination,'value',probe_destination)),
        (ValueType.Text,None,information_line_text),)
  rep=self.sndrcv("ProbeInstallCallback",*args)
  self.chk(rep)
  return (rep.status == tecrpc.Reply.Success)
 def ProbeInstallCallbackX(self,arg_list):
  args=((ValueType.Address,c_uint64,getattr(arg_list,'value',arg_list)),)
  rep=self.sndrcv("ProbeInstallCallbackX",*args)
  self.chk(rep)
  return (rep.status == tecrpc.Reply.Success)
 def ProbeIsCallbackInstalled(self):
  rep=self.sndrcv("ProbeIsCallbackInstalled")
  self.chk(rep)
  return rep.args[0].boolean
 def ProbeLinePlotGetDepValue(self,map_num):
  args=((ValueType.Scalar,c_int32,map_num),)
  rep=self.sndrcv("ProbeLinePlotGetDepValue",*args)
  self.chk(rep)
  return (
   (rep.status == tecrpc.Reply.Success),
   rep.args[0].float64)
 def ProbeLinePlotGetIndAxisKind(self):
  rep=self.sndrcv("ProbeLinePlotGetIndAxisKind")
  self.chk(rep)
  return rep.args[0].text[0]
 def ProbeLinePlotGetIndAxisNumber(self):
  rep=self.sndrcv("ProbeLinePlotGetIndAxisNumber")
  self.chk(rep)
  return rep.args[0].int32
 def ProbeLinePlotGetIndValue(self):
  rep=self.sndrcv("ProbeLinePlotGetIndValue")
  self.chk(rep)
  return rep.args[0].float64
 def ProbeLinePlotGetSourceMap(self):
  rep=self.sndrcv("ProbeLinePlotGetSourceMap")
  self.chk(rep)
  return rep.args[0].int32
 def ProbeOnSurface(self,num_points,x,y,z,zone_set,var_set,probe_nearest,obey_blanking,num_nearest_nodes,tolerance,values,cells_or_nodes,planes,zone_indices):
  args=((ValueType.Scalar,c_int64,num_points),
        (ValueType.Array,c_double,x),
        (ValueType.Array,c_double,y),
        (ValueType.Array,c_double,z),
        (ValueType.Address,c_uint64,getattr(zone_set,'value',zone_set)),
        (ValueType.Address,c_uint64,getattr(var_set,'value',var_set)),
        (ValueType.Scalar,c_int32,ProbeNearest(probe_nearest).value),
        (ValueType.Scalar,c_bool,obey_blanking),
        (ValueType.Scalar,c_int64,num_nearest_nodes),
        (ValueType.Scalar,c_double,tolerance),
        (ValueType.Array,c_double,values),
        (ValueType.Array,c_int64,cells_or_nodes),
        (ValueType.Array,c_int32,planes),
        (ValueType.Array,c_int32,zone_indices),)
  rep=self.sndrcv("ProbeOnSurface",*args)
  self.chk(rep)
  memmove(values, rep.args[0].buffer, sizeof(values))
  memmove(cells_or_nodes, rep.args[1].buffer, sizeof(cells_or_nodes))
  memmove(planes, rep.args[2].buffer, sizeof(planes))
  memmove(zone_indices, rep.args[3].buffer, sizeof(zone_indices))
  return (rep.status == tecrpc.Reply.Success)
 def ProbePerform(self,probe_info,callback):
  args=((ValueType.Address,c_uint64,getattr(probe_info,'value',probe_info)),
        (ValueType.Address,c_uint64,getattr(callback,'value',callback)),)
  rep=self.sndrcv("ProbePerform",*args)
  self.chk(rep)
  return (rep.status == tecrpc.Reply.Success)
 def ProbeRepeatLastEvent(self):
  rep=self.sndrcv("ProbeRepeatLastEvent")
  self.chk(rep)
  return (rep.status == tecrpc.Reply.Success)
 def PropagateLinking(self,link_type,frame_collection):
  args=((ValueType.Scalar,c_int32,LinkType(link_type).value),
        (ValueType.Scalar,c_int32,FrameCollection(frame_collection).value),)
  rep=self.sndrcv("PropagateLinking",*args)
  self.chk(rep)
  return (rep.status == tecrpc.Reply.Success)
 def Publish(self,f_name,include_layout_package,image_selection):
  args=((ValueType.Text,None,f_name),
        (ValueType.Scalar,c_bool,include_layout_package),
        (ValueType.Scalar,c_int32,ImageSelection(image_selection).value),)
  rep=self.sndrcv("Publish",*args)
  self.chk(rep)
  return (rep.status == tecrpc.Reply.Success)
 def QueryCanPlotIsoSurfaces(self):
  rep=self.sndrcv("QueryCanPlotIsoSurfaces")
  self.chk(rep)
  return rep.args[0].boolean
 def QueryCanPlotSlices(self):
  rep=self.sndrcv("QueryCanPlotSlices")
  self.chk(rep)
  return rep.args[0].boolean
 def QueryCanPlotStreamtraces(self):
  rep=self.sndrcv("QueryCanPlotStreamtraces")
  self.chk(rep)
  return rep.args[0].boolean
 def QueryCanPlotVolumeStreamtraces(self):
  rep=self.sndrcv("QueryCanPlotVolumeStreamtraces")
  self.chk(rep)
  return rep.args[0].boolean
 def QueryColorBandsInUseForContourGroup(self,contour_group):
  args=((ValueType.Scalar,c_int32,contour_group),)
  rep=self.sndrcv("QueryColorBandsInUseForContourGroup",*args)
  self.chk(rep)
  return rep.args[0].boolean
 def QueryContourLevelModificationsAllowed(self):
  rep=self.sndrcv("QueryContourLevelModificationsAllowed")
  self.chk(rep)
  return rep.args[0].boolean
 def QueryGetZoneRank(self,zone):
  args=((ValueType.Scalar,c_int32,zone),)
  rep=self.sndrcv("QueryGetZoneRank",*args)
  self.chk(rep)
  return rep.args[0].int32
 def QueryIsLayoutDirty(self):
  rep=self.sndrcv("QueryIsLayoutDirty")
  self.chk(rep)
  return rep.args[0].boolean
 def QueryIsTechnologyPreviewFeatureEnabled(self,feature):
  args=((ValueType.Text,None,feature),)
  rep=self.sndrcv("QueryIsTechnologyPreviewFeatureEnabled",*args)
  self.chk(rep)
  return rep.args[0].boolean
 def QueryIsXYDependentAllowedForFrame(self,frame_id):
  args=((ValueType.Scalar,c_int64,frame_id),)
  rep=self.sndrcv("QueryIsXYDependentAllowedForFrame",*args)
  self.chk(rep)
  return rep.args[0].boolean
 def QueryLayoutHasStyle(self):
  rep=self.sndrcv("QueryLayoutHasStyle")
  self.chk(rep)
  return rep.args[0].boolean
 def QueryOkToAnimateIJKPlanes(self):
  rep=self.sndrcv("QueryOkToAnimateIJKPlanes")
  self.chk(rep)
  return rep.args[0].boolean
 def QueryOkToAnimateZones(self):
  rep=self.sndrcv("QueryOkToAnimateZones")
  self.chk(rep)
  return rep.args[0].boolean
 def QueryOkToClearPickedObjects(self):
  rep=self.sndrcv("QueryOkToClearPickedObjects")
  self.chk(rep)
  return rep.args[0].boolean
 def QueryOkToCopyPickedObjects(self):
  rep=self.sndrcv("QueryOkToCopyPickedObjects")
  self.chk(rep)
  return rep.args[0].boolean
 def QueryOkToExtractContourLines(self):
  rep=self.sndrcv("QueryOkToExtractContourLines")
  self.chk(rep)
  return rep.args[0].boolean
 def QueryOkToExtractIsoSurfaces(self):
  rep=self.sndrcv("QueryOkToExtractIsoSurfaces")
  self.chk(rep)
  return rep.args[0].boolean
 def QueryOkToExtractPoints(self):
  rep=self.sndrcv("QueryOkToExtractPoints")
  self.chk(rep)
  return rep.args[0].boolean
 def QueryOkToExtractSlices(self):
  rep=self.sndrcv("QueryOkToExtractSlices")
  self.chk(rep)
  return rep.args[0].boolean
 def QueryOkToExtractStream(self):
  rep=self.sndrcv("QueryOkToExtractStream")
  self.chk(rep)
  return rep.args[0].boolean
 def QueryOkToPastePickedObjects(self):
  rep=self.sndrcv("QueryOkToPastePickedObjects")
  self.chk(rep)
  return rep.args[0].boolean
 def QueryOkToPushPopPickedObjects(self):
  rep=self.sndrcv("QueryOkToPushPopPickedObjects")
  self.chk(rep)
  return rep.args[0].boolean
 def QueryOkToSmooth(self):
  rep=self.sndrcv("QueryOkToSmooth")
  self.chk(rep)
  return rep.args[0].boolean
 def QueryPlotContainsContourLines(self):
  rep=self.sndrcv("QueryPlotContainsContourLines")
  self.chk(rep)
  return rep.args[0].boolean
 def QueryPlotContainsPoints(self):
  rep=self.sndrcv("QueryPlotContainsPoints")
  self.chk(rep)
  return rep.args[0].boolean
 def QueryPlotContainsSurfaceZones(self):
  rep=self.sndrcv("QueryPlotContainsSurfaceZones")
  self.chk(rep)
  return rep.args[0].boolean
 def QueryPlotContainsVolumeZones(self):
  rep=self.sndrcv("QueryPlotContainsVolumeZones")
  self.chk(rep)
  return rep.args[0].boolean
 def QueryStreamtracesAreActive(self):
  rep=self.sndrcv("QueryStreamtracesAreActive")
  self.chk(rep)
  return rep.args[0].boolean
 def QueryZoneCanPlotVolumeStreamtraces(self,zone):
  args=((ValueType.Scalar,c_int32,zone),)
  rep=self.sndrcv("QueryZoneCanPlotVolumeStreamtraces",*args)
  self.chk(rep)
  return rep.args[0].boolean
 def QueryZoneHasVisibleFieldStyle(self,zone):
  args=((ValueType.Scalar,c_int32,zone),)
  rep=self.sndrcv("QueryZoneHasVisibleFieldStyle",*args)
  self.chk(rep)
  return rep.args[0].boolean
 def Quit(self):
  rep=self.sndrcv("Quit")
  self.chk(rep)
  return (rep.status == tecrpc.Reply.Success)
 def QuitAddQueryCallback(self,quit_query_callback):
  args=((ValueType.Address,c_uint64,getattr(quit_query_callback,'value',quit_query_callback)),)
  rep=self.sndrcv("QuitAddQueryCallback",*args)
  self.chk(rep)
  return (rep.status == tecrpc.Reply.Success)
 def RawColorMap(self,num_raw_rgb_values,raw_r_values_array,raw_g_values_array,raw_b_values_array):
  args=((ValueType.Scalar,c_int32,num_raw_rgb_values),
        (ValueType.Array,c_uint8,raw_r_values_array),
        (ValueType.Array,c_uint8,raw_g_values_array),
        (ValueType.Array,c_uint8,raw_b_values_array),)
  rep=self.sndrcv("RawColorMap",*args)
  self.chk(rep)
  return (rep.status == tecrpc.Reply.Success)
 def ReadColorMap(self,f_name):
  args=((ValueType.Text,None,f_name),)
  rep=self.sndrcv("ReadColorMap",*args)
  self.chk(rep)
  return (rep.status == tecrpc.Reply.Success)
 def ReadDataSet(self,read_data_option,reset_style,file_names_or_instructions,data_set_reader,initial_plot_type,include_text,include_geom,include_custom_labels,include_data,collapse_zones_and_vars,zones_to_read,var_load_mode,var_position_list,var_name_list,i_skip,j_skip,k_skip):
  args=((ValueType.Scalar,c_int32,ReadDataOption(read_data_option).value),
        (ValueType.Scalar,c_bool,reset_style),
        (ValueType.Address,c_uint64,getattr(file_names_or_instructions,'value',file_names_or_instructions)),
        (ValueType.Text,None,data_set_reader),
        (ValueType.Scalar,c_int32,PlotType(initial_plot_type).value),
        (ValueType.Scalar,c_bool,include_text),
        (ValueType.Scalar,c_bool,include_geom),
        (ValueType.Scalar,c_bool,include_custom_labels),
        (ValueType.Scalar,c_bool,include_data),
        (ValueType.Scalar,c_bool,collapse_zones_and_vars),
        (ValueType.Address,c_uint64,getattr(zones_to_read,'value',zones_to_read)),
        (ValueType.Scalar,c_int32,VarLoadMode(var_load_mode).value),
        (ValueType.Address,c_uint64,getattr(var_position_list,'value',var_position_list)),
        (ValueType.Address,c_uint64,getattr(var_name_list,'value',var_name_list)),
        (ValueType.Scalar,c_int64,i_skip),
        (ValueType.Scalar,c_int64,j_skip),
        (ValueType.Scalar,c_int64,k_skip),)
  rep=self.sndrcv("ReadDataSet",*args)
  self.chk(rep)
  return (rep.status == tecrpc.Reply.Success)
 def ReadStylesheet(self,f_name,include_plot_style,include_text,include_geom,include_stream_positions,include_contour_levels,merge_style,include_frame_size_and_position):
  args=((ValueType.Text,None,f_name),
        (ValueType.Scalar,c_bool,include_plot_style),
        (ValueType.Scalar,c_bool,include_text),
        (ValueType.Scalar,c_bool,include_geom),
        (ValueType.Scalar,c_bool,include_stream_positions),
        (ValueType.Scalar,c_bool,include_contour_levels),
        (ValueType.Scalar,c_bool,merge_style),
        (ValueType.Scalar,c_bool,include_frame_size_and_position),)
  rep=self.sndrcv("ReadStylesheet",*args)
  self.chk(rep)
  return (rep.status == tecrpc.Reply.Success)
 def Redraw(self,do_full_drawing):
  args=((ValueType.Scalar,c_bool,do_full_drawing),)
  rep=self.sndrcv("Redraw",*args)
  self.chk(rep)
  return (rep.status == tecrpc.Reply.Success)
 def RedrawAll(self,do_full_drawing):
  args=((ValueType.Scalar,c_bool,do_full_drawing),)
  rep=self.sndrcv("RedrawAll",*args)
  self.chk(rep)
  return (rep.status == tecrpc.Reply.Success)
 def RegisterAbort(self,func):
  args=((ValueType.Address,c_uint64,getattr(func,'value',func)),)
  rep=self.sndrcv("RegisterAbort",*args)
  self.chk(rep)
 def Reset3DAngles(self):
  rep=self.sndrcv("Reset3DAngles")
  self.chk(rep)
 def Reset3DAxes(self):
  rep=self.sndrcv("Reset3DAxes")
  self.chk(rep)
  return (rep.status == tecrpc.Reply.Success)
 def Reset3DOrigin(self):
  rep=self.sndrcv("Reset3DOrigin")
  self.chk(rep)
  return (rep.status == tecrpc.Reply.Success)
 def Reset3DOriginX(self,arg_list):
  args=((ValueType.Address,c_uint64,getattr(arg_list,'value',arg_list)),)
  rep=self.sndrcv("Reset3DOriginX",*args)
  self.chk(rep)
  return (rep.status == tecrpc.Reply.Success)
 def Reset3DScaleFactors(self):
  rep=self.sndrcv("Reset3DScaleFactors")
  self.chk(rep)
  return (rep.status == tecrpc.Reply.Success)
 def ResetRefVectorMagnitude(self):
  rep=self.sndrcv("ResetRefVectorMagnitude")
  self.chk(rep)
  return (rep.status == tecrpc.Reply.Success)
 def ResetVectorLength(self):
  rep=self.sndrcv("ResetVectorLength")
  self.chk(rep)
  return (rep.status == tecrpc.Reply.Success)
 def ResetVectorSpacing(self):
  rep=self.sndrcv("ResetVectorSpacing")
  self.chk(rep)
  return (rep.status == tecrpc.Reply.Success)
 def RotateArbitrarySlice(self,axis,degrees,slice_group):
  args=((ValueType.Text,None,axis),
        (ValueType.Scalar,c_double,degrees),
        (ValueType.Scalar,c_int32,slice_group),)
  rep=self.sndrcv("RotateArbitrarySlice",*args)
  self.chk(rep)
 def RotateToSpecificAngles(self,psi,theta,alpha):
  args=((ValueType.Scalar,c_double,psi),
        (ValueType.Scalar,c_double,theta),
        (ValueType.Scalar,c_double,alpha),)
  rep=self.sndrcv("RotateToSpecificAngles",*args)
  self.chk(rep)
 def SaveLayout(self,f_name,use_relative_paths):
  args=((ValueType.Text,None,f_name),
        (ValueType.Scalar,c_bool,use_relative_paths),)
  rep=self.sndrcv("SaveLayout",*args)
  self.chk(rep)
  return (rep.status == tecrpc.Reply.Success)
 def SaveLayoutX(self,arg_list):
  args=((ValueType.Address,c_uint64,getattr(arg_list,'value',arg_list)),)
  rep=self.sndrcv("SaveLayoutX",*args)
  self.chk(rep)
  return (rep.status == tecrpc.Reply.Success)
 def ScatterResetRelSize(self):
  rep=self.sndrcv("ScatterResetRelSize")
  self.chk(rep)
  return (rep.status == tecrpc.Reply.Success)
 def ScriptExec(self,file_name):
  args=((ValueType.Text,None,file_name),)
  rep=self.sndrcv("ScriptExec",*args)
  self.chk(rep)
  return (rep.status == tecrpc.Reply.Success)
 def ScriptExecRegisterCallback(self,file_ext,script_language,script_exec_callback,client_data):
  args=((ValueType.Text,None,file_ext),
        (ValueType.Text,None,script_language),
        (ValueType.Address,c_uint64,getattr(script_exec_callback,'value',script_exec_callback)),
        (ValueType.ArbParam,None,client_data),)
  rep=self.sndrcv("ScriptExecRegisterCallback",*args)
  self.chk(rep)
  return (rep.status == tecrpc.Reply.Success)
 def ScriptProcessorGetClientData(self,script_extension):
  args=((ValueType.Text,None,script_extension),)
  rep=self.sndrcv("ScriptProcessorGetClientData",*args)
  self.chk(rep)
  return (
   (rep.status == tecrpc.Reply.Success),
   self.read_arbparam(rep.args[0]))
 def Set3DEyeDistance(self,eye_distance):
  args=((ValueType.Scalar,c_double,eye_distance),)
  rep=self.sndrcv("Set3DEyeDistance",*args)
  self.chk(rep)
  return (rep.status == tecrpc.Reply.Success)
 def SetAddMember(self,set,member,show_err):
  args=((ValueType.Address,c_uint64,getattr(set,'value',set)),
        (ValueType.Scalar,c_int64,member),
        (ValueType.Scalar,c_bool,show_err),)
  rep=self.sndrcv("SetAddMember",*args)
  self.chk(rep)
  return (rep.status == tecrpc.Reply.Success)
 def SetAlloc(self,show_err):
  args=((ValueType.Scalar,c_bool,show_err),)
  rep=self.sndrcv("SetAlloc",*args)
  self.chk(rep)
  return rep.args[0].uint64
 def SetClear(self,set):
  args=((ValueType.Address,c_uint64,getattr(set,'value',set)),)
  rep=self.sndrcv("SetClear",*args)
  self.chk(rep)
 def SetCopy(self,dst_set,src_set,show_err):
  args=((ValueType.Address,c_uint64,getattr(dst_set,'value',dst_set)),
        (ValueType.Address,c_uint64,getattr(src_set,'value',src_set)),
        (ValueType.Scalar,c_bool,show_err),)
  rep=self.sndrcv("SetCopy",*args)
  self.chk(rep)
  return (rep.status == tecrpc.Reply.Success)
 def SetDealloc(self,set):
  args=((ValueType.Address,c_uint64,set.contents.value),)
  rep=self.sndrcv("SetDealloc",*args)
  self.chk(rep)
  return rep.args[0].uint64
 def SetGetMember(self,set,position):
  args=((ValueType.Address,c_uint64,getattr(set,'value',set)),
        (ValueType.Scalar,c_int64,position),)
  rep=self.sndrcv("SetGetMember",*args)
  self.chk(rep)
  return rep.args[0].int64
 def SetGetMemberCount(self,set):
  args=((ValueType.Address,c_uint64,getattr(set,'value',set)),)
  rep=self.sndrcv("SetGetMemberCount",*args)
  self.chk(rep)
  return rep.args[0].int64
 def SetGetNextMember(self,set,member):
  args=((ValueType.Address,c_uint64,getattr(set,'value',set)),
        (ValueType.Scalar,c_int64,member),)
  rep=self.sndrcv("SetGetNextMember",*args)
  self.chk(rep)
  return rep.args[0].int64
 def SetGetPosition(self,set,member):
  args=((ValueType.Address,c_uint64,getattr(set,'value',set)),
        (ValueType.Scalar,c_int64,member),)
  rep=self.sndrcv("SetGetPosition",*args)
  self.chk(rep)
  return rep.args[0].int64
 def SetGetPrevMember(self,set,member):
  args=((ValueType.Address,c_uint64,getattr(set,'value',set)),
        (ValueType.Scalar,c_int64,member),)
  rep=self.sndrcv("SetGetPrevMember",*args)
  self.chk(rep)
  return rep.args[0].int64
 def SetIsEmpty(self,set):
  args=((ValueType.Address,c_uint64,getattr(set,'value',set)),)
  rep=self.sndrcv("SetIsEmpty",*args)
  self.chk(rep)
  return rep.args[0].boolean
 def SetIsEqual(self,set1,set2):
  args=((ValueType.Address,c_uint64,getattr(set1,'value',set1)),
        (ValueType.Address,c_uint64,getattr(set2,'value',set2)),)
  rep=self.sndrcv("SetIsEqual",*args)
  self.chk(rep)
  return rep.args[0].boolean
 def SetIsMember(self,set,member):
  args=((ValueType.Address,c_uint64,getattr(set,'value',set)),
        (ValueType.Scalar,c_int64,member),)
  rep=self.sndrcv("SetIsMember",*args)
  self.chk(rep)
  return rep.args[0].boolean
 def SetRemoveMember(self,set,member):
  args=((ValueType.Address,c_uint64,getattr(set,'value',set)),
        (ValueType.Scalar,c_int64,member),)
  rep=self.sndrcv("SetRemoveMember",*args)
  self.chk(rep)
 def SetupTransformations(self):
  rep=self.sndrcv("SetupTransformations")
  self.chk(rep)
 def SliceFinishDragging(self):
  rep=self.sndrcv("SliceFinishDragging")
  self.chk(rep)
 def SliceSetArbitraryUsingThreePoints(self,frame_id,slice_group,x1,y1,z1,x2,y2,z2,x3,y3,z3):
  args=((ValueType.Scalar,c_int64,frame_id),
        (ValueType.Scalar,c_int32,slice_group),
        (ValueType.Scalar,c_double,x1),
        (ValueType.Scalar,c_double,y1),
        (ValueType.Scalar,c_double,z1),
        (ValueType.Scalar,c_double,x2),
        (ValueType.Scalar,c_double,y2),
        (ValueType.Scalar,c_double,z2),
        (ValueType.Scalar,c_double,x3),
        (ValueType.Scalar,c_double,y3),
        (ValueType.Scalar,c_double,z3),)
  rep=self.sndrcv("SliceSetArbitraryUsingThreePoints",*args)
  self.chk(rep)
  return (rep.status == tecrpc.Reply.Success)
 def SliceSolidPlaneSetPosition(self,slice_position):
  args=((ValueType.Scalar,c_double,slice_position),)
  rep=self.sndrcv("SliceSolidPlaneSetPosition",*args)
  self.chk(rep)
  return rep.args[0].float64
 def SliceStartDragging(self):
  rep=self.sndrcv("SliceStartDragging")
  self.chk(rep)
 def Smooth(self,zone,smooth_var,num_smooth_passes,smooth_weight,smooth_bndry_cond):
  args=((ValueType.Scalar,c_int32,zone),
        (ValueType.Scalar,c_int32,smooth_var),
        (ValueType.Scalar,c_int32,num_smooth_passes),
        (ValueType.Scalar,c_double,smooth_weight),
        (ValueType.Scalar,c_int32,BoundaryCondition(smooth_bndry_cond).value),)
  rep=self.sndrcv("Smooth",*args)
  self.chk(rep)
  return (rep.status == tecrpc.Reply.Success)
 def SolutionTimeGetCurrent(self):
  rep=self.sndrcv("SolutionTimeGetCurrent")
  self.chk(rep)
  return rep.args[0].float64
 def SolutionTimeGetCurrentForFrame(self,frame_id):
  args=((ValueType.Scalar,c_int64,frame_id),)
  rep=self.sndrcv("SolutionTimeGetCurrentForFrame",*args)
  self.chk(rep)
  return rep.args[0].float64
 def SolutionTimeGetCurrentTimeStepForFrame(self,frame_id):
  args=((ValueType.Scalar,c_int64,frame_id),)
  rep=self.sndrcv("SolutionTimeGetCurrentTimeStepForFrame",*args)
  self.chk(rep)
  return (
   (rep.status == tecrpc.Reply.Success),
   rep.args[0].int32)
 def SolutionTimeGetMax(self):
  rep=self.sndrcv("SolutionTimeGetMax")
  self.chk(rep)
  return rep.args[0].float64
 def SolutionTimeGetMin(self):
  rep=self.sndrcv("SolutionTimeGetMin")
  self.chk(rep)
  return rep.args[0].float64
 def SolutionTimeGetNumTimeStepsByDataSetID(self,data_set_id):
  args=((ValueType.Scalar,c_int64,data_set_id),)
  rep=self.sndrcv("SolutionTimeGetNumTimeStepsByDataSetID",*args)
  self.chk(rep)
  return (
   (rep.status == tecrpc.Reply.Success),
   rep.args[0].int32)
 def SolutionTimeGetNumTimeStepsForFrame(self,frame_id):
  args=((ValueType.Scalar,c_int64,frame_id),)
  rep=self.sndrcv("SolutionTimeGetNumTimeStepsForFrame",*args)
  self.chk(rep)
  return (
   (rep.status == tecrpc.Reply.Success),
   rep.args[0].int32)
 def SolutionTimeGetSolutionTimeAtTimeStepByDataSetID(self,data_set_id,time_step):
  args=((ValueType.Scalar,c_int64,data_set_id),
        (ValueType.Scalar,c_int32,time_step),)
  rep=self.sndrcv("SolutionTimeGetSolutionTimeAtTimeStepByDataSetID",*args)
  self.chk(rep)
  return (
   (rep.status == tecrpc.Reply.Success),
   rep.args[0].float64)
 def SolutionTimeGetSolutionTimeAtTimeStepForFrame(self,frame_id,time_step):
  args=((ValueType.Scalar,c_int64,frame_id),
        (ValueType.Scalar,c_int32,time_step),)
  rep=self.sndrcv("SolutionTimeGetSolutionTimeAtTimeStepForFrame",*args)
  self.chk(rep)
  return (
   (rep.status == tecrpc.Reply.Success),
   rep.args[0].float64)
 def SolutionTimeGetSolutionTimeMinMaxByDataSetID(self,data_set_id):
  args=((ValueType.Scalar,c_int64,data_set_id),)
  rep=self.sndrcv("SolutionTimeGetSolutionTimeMinMaxByDataSetID",*args)
  self.chk(rep)
  return (
   (rep.status == tecrpc.Reply.Success),
   rep.args[0].float64,
   rep.args[1].float64)
 def SolutionTimeGetSolutionTimeMinMaxForFrame(self,frame_id):
  args=((ValueType.Scalar,c_int64,frame_id),)
  rep=self.sndrcv("SolutionTimeGetSolutionTimeMinMaxForFrame",*args)
  self.chk(rep)
  return (
   (rep.status == tecrpc.Reply.Success),
   rep.args[0].float64,
   rep.args[1].float64)
 def SolutionTimeGetSolutionTimesByDataSetID(self,data_set_id):
  args=((ValueType.Scalar,c_int64,data_set_id),)
  rep=self.sndrcv("SolutionTimeGetSolutionTimesByDataSetID",*args)
  self.chk(rep)
  return (
   (rep.status == tecrpc.Reply.Success),
   len(rep.args[0].buffer)//sizeof(c_double),
   self.read_array(rep.args[0], c_double))
 def SolutionTimeGetSolutionTimesForFrame(self,frame_id):
  args=((ValueType.Scalar,c_int64,frame_id),)
  rep=self.sndrcv("SolutionTimeGetSolutionTimesForFrame",*args)
  self.chk(rep)
  return (
   (rep.status == tecrpc.Reply.Success),
   len(rep.args[0].buffer)//sizeof(c_double),
   self.read_array(rep.args[0], c_double))
 def SolutionTimeGetTimeStepAtSolutionTimeByDataSetID(self,data_set_id,solution_time):
  args=((ValueType.Scalar,c_int64,data_set_id),
        (ValueType.Scalar,c_double,solution_time),)
  rep=self.sndrcv("SolutionTimeGetTimeStepAtSolutionTimeByDataSetID",*args)
  self.chk(rep)
  return (
   (rep.status == tecrpc.Reply.Success),
   rep.args[0].int32)
 def SolutionTimeGetTimeStepAtSolutionTimeForFrame(self,frame_id,solution_time):
  args=((ValueType.Scalar,c_int64,frame_id),
        (ValueType.Scalar,c_double,solution_time),)
  rep=self.sndrcv("SolutionTimeGetTimeStepAtSolutionTimeForFrame",*args)
  self.chk(rep)
  return (
   (rep.status == tecrpc.Reply.Success),
   rep.args[0].int32)
 def SolutionTimeSetCurrent(self,new_solution_time):
  args=((ValueType.Scalar,c_double,new_solution_time),)
  rep=self.sndrcv("SolutionTimeSetCurrent",*args)
  self.chk(rep)
  return try_cast_to_enum(SetValueReturnCode, rep.args[0].int32)
 def SortUInt32ItemArray(self,item_array,item_count,item_comparator,client_data):
  args=((ValueType.Array,c_uint32,item_array),
        (ValueType.Scalar,c_uint64,item_count),
        (ValueType.Address,c_uint64,getattr(item_comparator,'value',item_comparator)),
        (ValueType.ArbParam,None,client_data),)
  rep=self.sndrcv("SortUInt32ItemArray",*args)
  self.chk(rep)
  return cast(rep.args[0].buffer, POINTER(c_uint32))
 def SortUInt64ItemArray(self,item_array,item_count,item_comparator,client_data):
  args=((ValueType.Array,c_uint64,item_array),
        (ValueType.Scalar,c_uint64,item_count),
        (ValueType.Address,c_uint64,getattr(item_comparator,'value',item_comparator)),
        (ValueType.ArbParam,None,client_data),)
  rep=self.sndrcv("SortUInt64ItemArray",*args)
  self.chk(rep)
  return cast(rep.args[0].buffer, POINTER(c_uint64))
 def StateChangeAddCallback(self,state_change_callback):
  args=((ValueType.Address,c_uint64,getattr(state_change_callback,'value',state_change_callback)),)
  rep=self.sndrcv("StateChangeAddCallback",*args)
  self.chk(rep)
  return (rep.status == tecrpc.Reply.Success)
 def StateChangeAddCallbackX(self,arg_list):
  args=((ValueType.Address,c_uint64,getattr(arg_list,'value',arg_list)),)
  rep=self.sndrcv("StateChangeAddCallbackX",*args)
  self.chk(rep)
  return (rep.status == tecrpc.Reply.Success)
 def StateChangeGetArbEnum(self):
  rep=self.sndrcv("StateChangeGetArbEnum")
  self.chk(rep)
  return (
   (rep.status == tecrpc.Reply.Success),
   rep.args[0].int32)
 def StateChangeGetDataSetUniqueID(self):
  rep=self.sndrcv("StateChangeGetDataSetUniqueID")
  self.chk(rep)
  return (
   (rep.status == tecrpc.Reply.Success),
   rep.args[0].int64)
 def StateChangeGetFrameUniqueID(self):
  rep=self.sndrcv("StateChangeGetFrameUniqueID")
  self.chk(rep)
  return (
   (rep.status == tecrpc.Reply.Success),
   rep.args[0].int64)
 def StateChangeGetIndex(self):
  rep=self.sndrcv("StateChangeGetIndex")
  self.chk(rep)
  return (
   (rep.status == tecrpc.Reply.Success),
   rep.args[0].int64)
 def StateChangeGetInfoX(self,arg_list):
  args=((ValueType.Address,c_uint64,getattr(arg_list,'value',arg_list)),)
  rep=self.sndrcv("StateChangeGetInfoX",*args)
  self.chk(rep)
 def StateChangeGetMap(self):
  rep=self.sndrcv("StateChangeGetMap")
  self.chk(rep)
  return (
   (rep.status == tecrpc.Reply.Success),
   rep.args[0].int32)
 def StateChangeGetName(self):
  rep=self.sndrcv("StateChangeGetName")
  self.chk(rep)
  return (
   (rep.status == tecrpc.Reply.Success),
   self.read_text(rep.args[0]))
 def StateChangeGetPageUniqueID(self):
  rep=self.sndrcv("StateChangeGetPageUniqueID")
  self.chk(rep)
  return (
   (rep.status == tecrpc.Reply.Success),
   rep.args[0].int64)
 def StateChangeGetStyleParam(self,param):
  args=((ValueType.Scalar,c_int32,param),)
  rep=self.sndrcv("StateChangeGetStyleParam",*args)
  self.chk(rep)
  return (
   (rep.status == tecrpc.Reply.Success),
   self.read_text(rep.args[0]))
 def StateChangeGetUniqueID(self):
  rep=self.sndrcv("StateChangeGetUniqueID")
  self.chk(rep)
  return (
   (rep.status == tecrpc.Reply.Success),
   rep.args[0].int64)
 def StateChangeGetVar(self):
  rep=self.sndrcv("StateChangeGetVar")
  self.chk(rep)
  return (
   (rep.status == tecrpc.Reply.Success),
   rep.args[0].int32)
 def StateChangeGetVarSet(self):
  rep=self.sndrcv("StateChangeGetVarSet")
  self.chk(rep)
  return (
   (rep.status == tecrpc.Reply.Success),
   rep.args[0].uint64)
 def StateChangeGetZone(self):
  rep=self.sndrcv("StateChangeGetZone")
  self.chk(rep)
  return (
   (rep.status == tecrpc.Reply.Success),
   rep.args[0].int32)
 def StateChangeGetZoneSet(self):
  rep=self.sndrcv("StateChangeGetZoneSet")
  self.chk(rep)
  return (
   (rep.status == tecrpc.Reply.Success),
   rep.args[0].uint64)
 def StateChangeRemoveCBX(self,arg_list):
  args=((ValueType.Address,c_uint64,getattr(arg_list,'value',arg_list)),)
  rep=self.sndrcv("StateChangeRemoveCBX",*args)
  self.chk(rep)
  return (rep.status == tecrpc.Reply.Success)
 def StateChangeRemoveCallback(self,add_on_state_change_callback):
  args=((ValueType.Address,c_uint64,add_on_state_change_callback.contents.value),)
  rep=self.sndrcv("StateChangeRemoveCallback",*args)
  self.chk(rep)
  return (rep.status == tecrpc.Reply.Success)
 def StateChangeSetMode(self,callback,mode):
  args=((ValueType.Address,c_uint64,getattr(callback,'value',callback)),
        (ValueType.Scalar,c_int32,StateChangeMode(mode).value),)
  rep=self.sndrcv("StateChangeSetMode",*args)
  self.chk(rep)
  return (rep.status == tecrpc.Reply.Success)
 def StateChanged(self,state_change,call_data):
  args=((ValueType.Scalar,c_int32,StateChange(state_change).value),
        (ValueType.ArbParam,None,call_data),)
  rep=self.sndrcv("StateChanged",*args)
  self.chk(rep)
 def StateChangedX(self,arg_list):
  args=((ValueType.Address,c_uint64,getattr(arg_list,'value',arg_list)),)
  rep=self.sndrcv("StateChangedX",*args)
  self.chk(rep)
 def StateIsProcessingJournal(self):
  rep=self.sndrcv("StateIsProcessingJournal")
  self.chk(rep)
  return rep.args[0].boolean
 def StateIsProcessingLayout(self):
  rep=self.sndrcv("StateIsProcessingLayout")
  self.chk(rep)
  return rep.args[0].boolean
 def StateIsProcessingMacro(self):
  rep=self.sndrcv("StateIsProcessingMacro")
  self.chk(rep)
  return rep.args[0].boolean
 def StateIsProcessingStylesheet(self):
  rep=self.sndrcv("StateIsProcessingStylesheet")
  self.chk(rep)
  return rep.args[0].boolean
 def StatusCheckPercentDone(self,percent_done):
  args=((ValueType.Scalar,c_int32,percent_done),)
  rep=self.sndrcv("StatusCheckPercentDone",*args)
  self.chk(rep)
  return (rep.status == tecrpc.Reply.Success)
 def StatusFinishPercentDone(self):
  rep=self.sndrcv("StatusFinishPercentDone")
  self.chk(rep)
 def StatusSetPercentDoneText(self,percent_done_text):
  args=((ValueType.Text,None,percent_done_text),)
  rep=self.sndrcv("StatusSetPercentDoneText",*args)
  self.chk(rep)
 def StatusStartPercentDone(self,percent_done_text,show_stop_button,show_progress_bar):
  args=((ValueType.Text,None,percent_done_text),
        (ValueType.Scalar,c_bool,show_stop_button),
        (ValueType.Scalar,c_bool,show_progress_bar),)
  rep=self.sndrcv("StatusStartPercentDone",*args)
  self.chk(rep)
 def StatusSuspend(self,do_suspend):
  args=((ValueType.Scalar,c_bool,do_suspend),)
  rep=self.sndrcv("StatusSuspend",*args)
  self.chk(rep)
 def StreamtraceAdd(self,num_rake_points,stream_type,direction,start_x_pos,start_y_pos,start_z_pos,alt_start_x_pos,alt_start_y_pos,alt_start_z_pos):
  args=((ValueType.Scalar,c_int32,num_rake_points),
        (ValueType.Scalar,c_int32,Streamtrace(stream_type).value),
        (ValueType.Scalar,c_int32,StreamDir(direction).value),
        (ValueType.Scalar,c_double,start_x_pos),
        (ValueType.Scalar,c_double,start_y_pos),
        (ValueType.Scalar,c_double,start_z_pos),
        (ValueType.Scalar,c_double,alt_start_x_pos),
        (ValueType.Scalar,c_double,alt_start_y_pos),
        (ValueType.Scalar,c_double,alt_start_z_pos),)
  rep=self.sndrcv("StreamtraceAdd",*args)
  self.chk(rep)
  return (rep.status == tecrpc.Reply.Success)
 def StreamtraceAddX(self,arg_list):
  args=((ValueType.Address,c_uint64,getattr(arg_list,'value',arg_list)),)
  rep=self.sndrcv("StreamtraceAddX",*args)
  self.chk(rep)
  return (rep.status == tecrpc.Reply.Success)
 def StreamtraceDeleteAll(self):
  rep=self.sndrcv("StreamtraceDeleteAll")
  self.chk(rep)
  return (rep.status == tecrpc.Reply.Success)
 def StreamtraceDeleteRange(self,start,end):
  args=((ValueType.Scalar,c_int32,start),
        (ValueType.Scalar,c_int32,end),)
  rep=self.sndrcv("StreamtraceDeleteRange",*args)
  self.chk(rep)
  return (rep.status == tecrpc.Reply.Success)
 def StreamtraceGetCount(self):
  rep=self.sndrcv("StreamtraceGetCount")
  self.chk(rep)
  return rep.args[0].int32
 def StreamtraceGetPos(self,stream_number):
  args=((ValueType.Scalar,c_int32,stream_number),)
  rep=self.sndrcv("StreamtraceGetPos",*args)
  self.chk(rep)
  return (
   rep.args[0].float64,
   rep.args[1].float64,
   rep.args[2].float64)
 def StreamtraceGetType(self,stream_number):
  args=((ValueType.Scalar,c_int32,stream_number),)
  rep=self.sndrcv("StreamtraceGetType",*args)
  self.chk(rep)
  return try_cast_to_enum(Streamtrace, rep.args[0].int32)
 def StreamtraceHasTermLine(self):
  rep=self.sndrcv("StreamtraceHasTermLine")
  self.chk(rep)
  return rep.args[0].boolean
 def StreamtraceResetDelta(self):
  rep=self.sndrcv("StreamtraceResetDelta")
  self.chk(rep)
  return (rep.status == tecrpc.Reply.Success)
 def StreamtraceSetTermLine(self,num_points,x_term_line_pts_array,y_term_line_pts_array):
  args=((ValueType.Scalar,c_int32,num_points),
        (ValueType.Array,c_double,x_term_line_pts_array),
        (ValueType.Array,c_double,y_term_line_pts_array),)
  rep=self.sndrcv("StreamtraceSetTermLine",*args)
  self.chk(rep)
  return (rep.status == tecrpc.Reply.Success)
 def StringAlloc(self,max_length,debug_info):
  args=((ValueType.Scalar,c_int64,max_length),
        (ValueType.Text,None,debug_info),)
  rep=self.sndrcv("StringAlloc",*args)
  self.chk(rep)
  return self.read_text(rep.args[0])
 def StringConvOldFormatting(self,old_string,base_font):
  args=((ValueType.Text,None,old_string),
        (ValueType.Scalar,c_int32,Font(base_font).value),)
  rep=self.sndrcv("StringConvOldFormatting",*args)
  self.chk(rep)
  return self.read_text(rep.args[0])
 def StringDealloc(self,s):
  args=((ValueType.Address,c_uint64,s.contents.value),)
  rep=self.sndrcv("StringDealloc",*args)
  self.chk(rep)
  return self.read_text(rep.args[0])
 def StringFormatTimeDate(self,time_date_value,time_date_format):
  args=((ValueType.Scalar,c_double,time_date_value),
        (ValueType.Text,None,time_date_format),)
  rep=self.sndrcv("StringFormatTimeDate",*args)
  self.chk(rep)
  return self.read_text(rep.args[0])
 def StringFormatValue(self,value,format,precision):
  args=((ValueType.Scalar,c_double,value),
        (ValueType.Scalar,c_int32,NumberFormat(format).value),
        (ValueType.Scalar,c_int32,precision),)
  rep=self.sndrcv("StringFormatValue",*args)
  self.chk(rep)
  return self.read_text(rep.args[0])
 def StringListAlloc(self):
  rep=self.sndrcv("StringListAlloc")
  self.chk(rep)
  return rep.args[0].uint64
 def StringListAppend(self,target,source):
  args=((ValueType.Address,c_uint64,getattr(target,'value',target)),
        (ValueType.Address,c_uint64,getattr(source,'value',source)),)
  rep=self.sndrcv("StringListAppend",*args)
  self.chk(rep)
  return (rep.status == tecrpc.Reply.Success)
 def StringListAppendString(self,string_list,string):
  args=((ValueType.Address,c_uint64,getattr(string_list,'value',string_list)),
        (ValueType.Text,None,string),)
  rep=self.sndrcv("StringListAppendString",*args)
  self.chk(rep)
  return (rep.status == tecrpc.Reply.Success)
 def StringListClear(self,string_list):
  args=((ValueType.Address,c_uint64,getattr(string_list,'value',string_list)),)
  rep=self.sndrcv("StringListClear",*args)
  self.chk(rep)
 def StringListCopy(self,string_list):
  args=((ValueType.Address,c_uint64,getattr(string_list,'value',string_list)),)
  rep=self.sndrcv("StringListCopy",*args)
  self.chk(rep)
  return rep.args[0].uint64
 def StringListDealloc(self,string_list):
  args=((ValueType.Address,c_uint64,string_list.contents.value),)
  rep=self.sndrcv("StringListDealloc",*args)
  self.chk(rep)
  return rep.args[0].uint64
 def StringListFromNLString(self,string):
  args=((ValueType.Text,None,string),)
  rep=self.sndrcv("StringListFromNLString",*args)
  self.chk(rep)
  return rep.args[0].uint64
 def StringListGetCount(self,string_list):
  args=((ValueType.Address,c_uint64,getattr(string_list,'value',string_list)),)
  rep=self.sndrcv("StringListGetCount",*args)
  self.chk(rep)
  return rep.args[0].int64
 def StringListGetRawStringPtr(self,string_list,string_number):
  args=((ValueType.Address,c_uint64,getattr(string_list,'value',string_list)),
        (ValueType.Scalar,c_int64,string_number),)
  rep=self.sndrcv("StringListGetRawStringPtr",*args)
  self.chk(rep)
  return self.read_text(rep.args[0])
 def StringListGetString(self,string_list,string_number):
  args=((ValueType.Address,c_uint64,getattr(string_list,'value',string_list)),
        (ValueType.Scalar,c_int64,string_number),)
  rep=self.sndrcv("StringListGetString",*args)
  self.chk(rep)
  return self.read_text(rep.args[0])
 def StringListInsertString(self,string_list,string_number,string):
  args=((ValueType.Address,c_uint64,getattr(string_list,'value',string_list)),
        (ValueType.Scalar,c_int64,string_number),
        (ValueType.Text,None,string),)
  rep=self.sndrcv("StringListInsertString",*args)
  self.chk(rep)
  return (rep.status == tecrpc.Reply.Success)
 def StringListRemoveString(self,string_list,string_number):
  args=((ValueType.Address,c_uint64,getattr(string_list,'value',string_list)),
        (ValueType.Scalar,c_int64,string_number),)
  rep=self.sndrcv("StringListRemoveString",*args)
  self.chk(rep)
 def StringListRemoveStrings(self,string_list,string_number,count):
  args=((ValueType.Address,c_uint64,getattr(string_list,'value',string_list)),
        (ValueType.Scalar,c_int64,string_number),
        (ValueType.Scalar,c_int64,count),)
  rep=self.sndrcv("StringListRemoveStrings",*args)
  self.chk(rep)
 def StringListSetString(self,string_list,string_number,string):
  args=((ValueType.Address,c_uint64,getattr(string_list,'value',string_list)),
        (ValueType.Scalar,c_int64,string_number),
        (ValueType.Text,None,string),)
  rep=self.sndrcv("StringListSetString",*args)
  self.chk(rep)
  return (rep.status == tecrpc.Reply.Success)
 def StringListSort(self,string_list,comparator,client_data):
  args=((ValueType.Address,c_uint64,getattr(string_list,'value',string_list)),
        (ValueType.Address,c_uint64,getattr(comparator,'value',comparator)),
        (ValueType.ArbParam,None,client_data),)
  rep=self.sndrcv("StringListSort",*args)
  self.chk(rep)
 def StringListToNLString(self,string_list):
  args=((ValueType.Address,c_uint64,getattr(string_list,'value',string_list)),)
  rep=self.sndrcv("StringListToNLString",*args)
  self.chk(rep)
  return self.read_text(rep.args[0])
 def StyleGetLastErrorString(self):
  rep=self.sndrcv("StyleGetLastErrorString")
  self.chk(rep)
  return self.read_text(rep.args[0])
 def StyleGetLowLevelX(self,arg_list):
  args=((ValueType.Address,c_uint64,getattr(arg_list,'value',arg_list)),)
  rep=self.sndrcv("StyleGetLowLevelX",*args)
  self.chk(rep)
  return try_cast_to_enum(GetValueReturnCode, rep.args[0].int32)
 def StyleSetBase(self,style_base):
  args=((ValueType.Scalar,c_int32,StyleBase(style_base).value),)
  rep=self.sndrcv("StyleSetBase",*args)
  self.chk(rep)
  return (rep.status == tecrpc.Reply.Success)
 def StyleSetLowLevel(self,text_field_widget,d_value,i_value,set_or_offset,assign_modifier,p1,p2,p3,p4,p5,p6,do_implicit_recording):
  args=((ValueType.Scalar,c_double,d_value),
        (ValueType.ArbParam,None,i_value),
        (ValueType.ArbParam,None,set_or_offset),
        (ValueType.Scalar,c_int32,AssignOp(assign_modifier).value),
        (ValueType.Text,None,p1),
        (ValueType.Text,None,p2),
        (ValueType.Text,None,p3),
        (ValueType.Text,None,p4),
        (ValueType.Text,None,p5),
        (ValueType.Text,None,p6),
        (ValueType.Scalar,c_bool,do_implicit_recording),)
  rep=self.sndrcv("StyleSetLowLevel",*args)
  self.chk(rep)
  return try_cast_to_enum(SetValueReturnCode, rep.args[0].int32)
 def StyleSetLowLevelX(self,arg_list):
  args=((ValueType.Address,c_uint64,getattr(arg_list,'value',arg_list)),)
  rep=self.sndrcv("StyleSetLowLevelX",*args)
  self.chk(rep)
  return try_cast_to_enum(SetValueReturnCode, rep.args[0].int32)
 def StyleValueGetMacroID(self,style_value_name):
  args=((ValueType.Text,None,style_value_name),)
  rep=self.sndrcv("StyleValueGetMacroID",*args)
  self.chk(rep)
  return self.read_arbparam(rep.args[0])
 def System(self,command,wait):
  args=((ValueType.Text,None,command),
        (ValueType.Scalar,c_bool,wait),)
  rep=self.sndrcv("System",*args)
  self.chk(rep)
  return (rep.status == tecrpc.Reply.Success)
 def TecplotGetAppMode(self):
  rep=self.sndrcv("TecplotGetAppMode")
  self.chk(rep)
  return try_cast_to_enum(AppMode, rep.args[0].int32)
 def TecplotGetExePath(self):
  rep=self.sndrcv("TecplotGetExePath")
  self.chk(rep)
  return self.read_text(rep.args[0])
 def TecplotGetHomeDirectory(self):
  rep=self.sndrcv("TecplotGetHomeDirectory")
  self.chk(rep)
  return self.read_text(rep.args[0])
 def TecplotGetMajorRevision(self):
  rep=self.sndrcv("TecplotGetMajorRevision")
  self.chk(rep)
  return rep.args[0].int32
 def TecplotGetMajorVersion(self):
  rep=self.sndrcv("TecplotGetMajorVersion")
  self.chk(rep)
  return rep.args[0].int32
 def TecplotGetMinorRevision(self):
  rep=self.sndrcv("TecplotGetMinorRevision")
  self.chk(rep)
  return rep.args[0].int32
 def TecplotGetMinorVersion(self):
  rep=self.sndrcv("TecplotGetMinorVersion")
  self.chk(rep)
  return rep.args[0].int32
 def Text3DCreate(self,pos_x,pos_y,pos_z,height_units,height,text):
  args=((ValueType.Scalar,c_double,pos_x),
        (ValueType.Scalar,c_double,pos_y),
        (ValueType.Scalar,c_double,pos_z),
        (ValueType.Scalar,c_int32,Units(height_units).value),
        (ValueType.Scalar,c_double,height),
        (ValueType.Text,None,text),)
  rep=self.sndrcv("Text3DCreate",*args)
  self.chk(rep)
  return rep.args[0].int64
 def TextBoxGetColor(self,tid):
  args=((ValueType.Scalar,c_int64,tid),)
  rep=self.sndrcv("TextBoxGetColor",*args)
  self.chk(rep)
  return rep.args[0].int32
 def TextBoxGetFillColor(self,tid):
  args=((ValueType.Scalar,c_int64,tid),)
  rep=self.sndrcv("TextBoxGetFillColor",*args)
  self.chk(rep)
  return rep.args[0].int32
 def TextBoxGetLineThickness(self,tid):
  args=((ValueType.Scalar,c_int64,tid),)
  rep=self.sndrcv("TextBoxGetLineThickness",*args)
  self.chk(rep)
  return rep.args[0].float64
 def TextBoxGetMargin(self,tid):
  args=((ValueType.Scalar,c_int64,tid),)
  rep=self.sndrcv("TextBoxGetMargin",*args)
  self.chk(rep)
  return rep.args[0].float64
 def TextBoxGetPosition(self,t):
  args=((ValueType.Scalar,c_int64,t),)
  rep=self.sndrcv("TextBoxGetPosition",*args)
  self.chk(rep)
  return (
   rep.args[0].float64,
   rep.args[1].float64,
   rep.args[2].float64,
   rep.args[3].float64,
   rep.args[4].float64,
   rep.args[5].float64,
   rep.args[6].float64,
   rep.args[7].float64)
 def TextBoxGetType(self,tid):
  args=((ValueType.Scalar,c_int64,tid),)
  rep=self.sndrcv("TextBoxGetType",*args)
  self.chk(rep)
  return try_cast_to_enum(TextBox, rep.args[0].int32)
 def TextBoxSetColor(self,tid,box_color):
  args=((ValueType.Scalar,c_int64,tid),
        (ValueType.Scalar,c_int32,box_color),)
  rep=self.sndrcv("TextBoxSetColor",*args)
  self.chk(rep)
 def TextBoxSetFillColor(self,tid,box_fill_color):
  args=((ValueType.Scalar,c_int64,tid),
        (ValueType.Scalar,c_int32,box_fill_color),)
  rep=self.sndrcv("TextBoxSetFillColor",*args)
  self.chk(rep)
 def TextBoxSetLineThickness(self,tid,line_thickness):
  args=((ValueType.Scalar,c_int64,tid),
        (ValueType.Scalar,c_double,line_thickness),)
  rep=self.sndrcv("TextBoxSetLineThickness",*args)
  self.chk(rep)
 def TextBoxSetMargin(self,tid,margin):
  args=((ValueType.Scalar,c_int64,tid),
        (ValueType.Scalar,c_double,margin),)
  rep=self.sndrcv("TextBoxSetMargin",*args)
  self.chk(rep)
 def TextBoxSetType(self,tid,text_box_type):
  args=((ValueType.Scalar,c_int64,tid),
        (ValueType.Scalar,c_int32,TextBox(text_box_type).value),)
  rep=self.sndrcv("TextBoxSetType",*args)
  self.chk(rep)
 def TextCreate(self,position_coord_sys,pos_x,pos_y,height_units,height,text):
  args=((ValueType.Scalar,c_int32,CoordSys(position_coord_sys).value),
        (ValueType.Scalar,c_double,pos_x),
        (ValueType.Scalar,c_double,pos_y),
        (ValueType.Scalar,c_int32,Units(height_units).value),
        (ValueType.Scalar,c_double,height),
        (ValueType.Text,None,text),)
  rep=self.sndrcv("TextCreate",*args)
  self.chk(rep)
  return rep.args[0].int64
 def TextCreateX(self,arg_list):
  args=((ValueType.Address,c_uint64,getattr(arg_list,'value',arg_list)),)
  rep=self.sndrcv("TextCreateX",*args)
  self.chk(rep)
  return rep.args[0].int64
 def TextDelete(self,tid):
  args=((ValueType.Scalar,c_int64,tid),)
  rep=self.sndrcv("TextDelete",*args)
  self.chk(rep)
 def TextGetAnchor(self,tid):
  args=((ValueType.Scalar,c_int64,tid),)
  rep=self.sndrcv("TextGetAnchor",*args)
  self.chk(rep)
  return try_cast_to_enum(TextAnchor, rep.args[0].int32)
 def TextGetAnchorPos(self,tid):
  args=((ValueType.Scalar,c_int64,tid),)
  rep=self.sndrcv("TextGetAnchorPos",*args)
  self.chk(rep)
  return (
   rep.args[0].float64,
   rep.args[1].float64,
   rep.args[2].float64)
 def TextGetAngle(self,tid):
  args=((ValueType.Scalar,c_int64,tid),)
  rep=self.sndrcv("TextGetAngle",*args)
  self.chk(rep)
  return rep.args[0].float64
 def TextGetBase(self):
  rep=self.sndrcv("TextGetBase")
  self.chk(rep)
  return rep.args[0].int64
 def TextGetClipping(self,tid):
  args=((ValueType.Scalar,c_int64,tid),)
  rep=self.sndrcv("TextGetClipping",*args)
  self.chk(rep)
  return try_cast_to_enum(Clipping, rep.args[0].int32)
 def TextGetColor(self,tid):
  args=((ValueType.Scalar,c_int64,tid),)
  rep=self.sndrcv("TextGetColor",*args)
  self.chk(rep)
  return rep.args[0].int32
 def TextGetFont(self,tid):
  args=((ValueType.Scalar,c_int64,tid),)
  rep=self.sndrcv("TextGetFont",*args)
  self.chk(rep)
  return try_cast_to_enum(Font, rep.args[0].int32)
 def TextGetHeight(self,tid):
  args=((ValueType.Scalar,c_int64,tid),)
  rep=self.sndrcv("TextGetHeight",*args)
  self.chk(rep)
  return rep.args[0].float64
 def TextGetLineSpacing(self,tid):
  args=((ValueType.Scalar,c_int64,tid),)
  rep=self.sndrcv("TextGetLineSpacing",*args)
  self.chk(rep)
  return rep.args[0].float64
 def TextGetMacroFunctionCmd(self,tid):
  args=((ValueType.Scalar,c_int64,tid),)
  rep=self.sndrcv("TextGetMacroFunctionCmd",*args)
  self.chk(rep)
  return (
   (rep.status == tecrpc.Reply.Success),
   self.read_text(rep.args[0]))
 def TextGetNext(self,tid):
  args=((ValueType.Scalar,c_int64,tid),)
  rep=self.sndrcv("TextGetNext",*args)
  self.chk(rep)
  return rep.args[0].int64
 def TextGetPositionCoordSys(self,tid):
  args=((ValueType.Scalar,c_int64,tid),)
  rep=self.sndrcv("TextGetPositionCoordSys",*args)
  self.chk(rep)
  return try_cast_to_enum(CoordSys, rep.args[0].int32)
 def TextGetPrev(self,tid):
  args=((ValueType.Scalar,c_int64,tid),)
  rep=self.sndrcv("TextGetPrev",*args)
  self.chk(rep)
  return rep.args[0].int64
 def TextGetScope(self,tid):
  args=((ValueType.Scalar,c_int64,tid),)
  rep=self.sndrcv("TextGetScope",*args)
  self.chk(rep)
  return try_cast_to_enum(Scope, rep.args[0].int32)
 def TextGetSizeUnits(self,tid):
  args=((ValueType.Scalar,c_int64,tid),)
  rep=self.sndrcv("TextGetSizeUnits",*args)
  self.chk(rep)
  return try_cast_to_enum(Units, rep.args[0].int32)
 def TextGetString(self,tid):
  args=((ValueType.Scalar,c_int64,tid),)
  rep=self.sndrcv("TextGetString",*args)
  self.chk(rep)
  return (
   (rep.status == tecrpc.Reply.Success),
   self.read_text(rep.args[0]))
 def TextGetType(self,tid):
  args=((ValueType.Scalar,c_int64,tid),)
  rep=self.sndrcv("TextGetType",*args)
  self.chk(rep)
  return try_cast_to_enum(TextType, rep.args[0].int32)
 def TextGetTypefaceFamily(self,tid):
  args=((ValueType.Scalar,c_int64,tid),)
  rep=self.sndrcv("TextGetTypefaceFamily",*args)
  self.chk(rep)
  return self.read_text(rep.args[0])
 def TextGetTypefaceIsBold(self,tid):
  args=((ValueType.Scalar,c_int64,tid),)
  rep=self.sndrcv("TextGetTypefaceIsBold",*args)
  self.chk(rep)
  return rep.args[0].boolean
 def TextGetTypefaceIsItalic(self,tid):
  args=((ValueType.Scalar,c_int64,tid),)
  rep=self.sndrcv("TextGetTypefaceIsItalic",*args)
  self.chk(rep)
  return rep.args[0].boolean
 def TextGetZoneOrMap(self,tid):
  args=((ValueType.Scalar,c_int64,tid),)
  rep=self.sndrcv("TextGetZoneOrMap",*args)
  self.chk(rep)
  return rep.args[0].int32
 def TextIsAttached(self,tid):
  args=((ValueType.Scalar,c_int64,tid),)
  rep=self.sndrcv("TextIsAttached",*args)
  self.chk(rep)
  return rep.args[0].boolean
 def TextIsValid(self,tid):
  args=((ValueType.Scalar,c_int64,tid),)
  rep=self.sndrcv("TextIsValid",*args)
  self.chk(rep)
  return rep.args[0].boolean
 def TextSetAnchor(self,tid,anchor):
  args=((ValueType.Scalar,c_int64,tid),
        (ValueType.Scalar,c_int32,TextAnchor(anchor).value),)
  rep=self.sndrcv("TextSetAnchor",*args)
  self.chk(rep)
 def TextSetAnchorPos(self,tid,x_or_theta_pos,y_or_r_pos,z_pos):
  args=((ValueType.Scalar,c_int64,tid),
        (ValueType.Scalar,c_double,x_or_theta_pos),
        (ValueType.Scalar,c_double,y_or_r_pos),
        (ValueType.Scalar,c_double,z_pos),)
  rep=self.sndrcv("TextSetAnchorPos",*args)
  self.chk(rep)
 def TextSetAngle(self,tid,angle):
  args=((ValueType.Scalar,c_int64,tid),
        (ValueType.Scalar,c_double,angle),)
  rep=self.sndrcv("TextSetAngle",*args)
  self.chk(rep)
 def TextSetAttached(self,tid,attached):
  args=((ValueType.Scalar,c_int64,tid),
        (ValueType.Scalar,c_bool,attached),)
  rep=self.sndrcv("TextSetAttached",*args)
  self.chk(rep)
 def TextSetClipping(self,tid,clipping):
  args=((ValueType.Scalar,c_int64,tid),
        (ValueType.Scalar,c_int32,Clipping(clipping).value),)
  rep=self.sndrcv("TextSetClipping",*args)
  self.chk(rep)
 def TextSetColor(self,tid,color):
  args=((ValueType.Scalar,c_int64,tid),
        (ValueType.Scalar,c_int32,color),)
  rep=self.sndrcv("TextSetColor",*args)
  self.chk(rep)
 def TextSetCoordSysAndUnits(self,tid,position_coord_sys,height_units):
  args=((ValueType.Scalar,c_int64,tid),
        (ValueType.Scalar,c_int32,CoordSys(position_coord_sys).value),
        (ValueType.Scalar,c_int32,Units(height_units).value),)
  rep=self.sndrcv("TextSetCoordSysAndUnits",*args)
  self.chk(rep)
 def TextSetFont(self,tid,font):
  args=((ValueType.Scalar,c_int64,tid),
        (ValueType.Scalar,c_int32,Font(font).value),)
  rep=self.sndrcv("TextSetFont",*args)
  self.chk(rep)
 def TextSetHeight(self,tid,height):
  args=((ValueType.Scalar,c_int64,tid),
        (ValueType.Scalar,c_double,height),)
  rep=self.sndrcv("TextSetHeight",*args)
  self.chk(rep)
 def TextSetLineSpacing(self,tid,line_spacing):
  args=((ValueType.Scalar,c_int64,tid),
        (ValueType.Scalar,c_double,line_spacing),)
  rep=self.sndrcv("TextSetLineSpacing",*args)
  self.chk(rep)
 def TextSetMacroFunctionCmd(self,tid,command):
  args=((ValueType.Scalar,c_int64,tid),
        (ValueType.Text,None,command),)
  rep=self.sndrcv("TextSetMacroFunctionCmd",*args)
  self.chk(rep)
  return (rep.status == tecrpc.Reply.Success)
 def TextSetScope(self,tid,scope):
  args=((ValueType.Scalar,c_int64,tid),
        (ValueType.Scalar,c_int32,Scope(scope).value),)
  rep=self.sndrcv("TextSetScope",*args)
  self.chk(rep)
 def TextSetString(self,tid,text_string):
  args=((ValueType.Scalar,c_int64,tid),
        (ValueType.Text,None,text_string),)
  rep=self.sndrcv("TextSetString",*args)
  self.chk(rep)
  return (rep.status == tecrpc.Reply.Success)
 def TextSetType(self,tid,text_type):
  args=((ValueType.Scalar,c_int64,tid),
        (ValueType.Scalar,c_int32,TextType(text_type).value),)
  rep=self.sndrcv("TextSetType",*args)
  self.chk(rep)
 def TextSetTypeface(self,tid,font_family,is_bold,is_italic):
  args=((ValueType.Scalar,c_int64,tid),
        (ValueType.Text,None,font_family),
        (ValueType.Scalar,c_bool,is_bold),
        (ValueType.Scalar,c_bool,is_italic),)
  rep=self.sndrcv("TextSetTypeface",*args)
  self.chk(rep)
 def TextSetZoneOrMap(self,tid,zone_or_map):
  args=((ValueType.Scalar,c_int64,tid),
        (ValueType.Scalar,c_int32,zone_or_map),)
  rep=self.sndrcv("TextSetZoneOrMap",*args)
  self.chk(rep)
 def ThreadBroadcastCondition(self,condition):
  args=((ValueType.Address,c_uint64,getattr(condition,'value',condition)),)
  rep=self.sndrcv("ThreadBroadcastCondition",*args)
  self.chk(rep)
 def ThreadConditionAlloc(self):
  rep=self.sndrcv("ThreadConditionAlloc")
  self.chk(rep)
  return rep.args[0].uint64
 def ThreadConditionDealloc(self,condition):
  args=((ValueType.Address,c_uint64,condition.contents.value),)
  rep=self.sndrcv("ThreadConditionDealloc",*args)
  self.chk(rep)
  return rep.args[0].uint64
 def ThreadCreateDetached(self,thread_function,thread_data):
  args=((ValueType.Address,c_uint64,getattr(thread_function,'value',thread_function)),
        (ValueType.ArbParam,None,thread_data),)
  rep=self.sndrcv("ThreadCreateDetached",*args)
  self.chk(rep)
  return (rep.status == tecrpc.Reply.Success)
 def ThreadMutexAlloc(self):
  rep=self.sndrcv("ThreadMutexAlloc")
  self.chk(rep)
  return rep.args[0].uint64
 def ThreadMutexDealloc(self,mutex):
  args=((ValueType.Address,c_uint64,mutex.contents.value),)
  rep=self.sndrcv("ThreadMutexDealloc",*args)
  self.chk(rep)
  return rep.args[0].uint64
 def ThreadMutexLock(self,mutex):
  args=((ValueType.Address,c_uint64,getattr(mutex,'value',mutex)),)
  rep=self.sndrcv("ThreadMutexLock",*args)
  self.chk(rep)
 def ThreadMutexUnlock(self,mutex):
  args=((ValueType.Address,c_uint64,getattr(mutex,'value',mutex)),)
  rep=self.sndrcv("ThreadMutexUnlock",*args)
  self.chk(rep)
 def ThreadPoolAddJob(self,job,job_data,job_control):
  args=((ValueType.Address,c_uint64,getattr(job,'value',job)),
        (ValueType.ArbParam,None,job_data),
        (ValueType.Address,c_uint64,getattr(job_control,'value',job_control)),)
  rep=self.sndrcv("ThreadPoolAddJob",*args)
  self.chk(rep)
 def ThreadPoolJobControlAlloc(self):
  rep=self.sndrcv("ThreadPoolJobControlAlloc")
  self.chk(rep)
  return rep.args[0].uint64
 def ThreadPoolJobControlDealloc(self,job_control):
  args=((ValueType.Address,c_uint64,job_control.contents.value),)
  rep=self.sndrcv("ThreadPoolJobControlDealloc",*args)
  self.chk(rep)
  return rep.args[0].uint64
 def ThreadPoolJobThreadOffset(self):
  rep=self.sndrcv("ThreadPoolJobThreadOffset")
  self.chk(rep)
  return rep.args[0].int32
 def ThreadPoolPoolSize(self):
  rep=self.sndrcv("ThreadPoolPoolSize")
  self.chk(rep)
  return rep.args[0].int32
 def ThreadPoolWait(self,job_control):
  args=((ValueType.Address,c_uint64,getattr(job_control,'value',job_control)),)
  rep=self.sndrcv("ThreadPoolWait",*args)
  self.chk(rep)
 def ThreadRecursiveMutexAlloc(self):
  rep=self.sndrcv("ThreadRecursiveMutexAlloc")
  self.chk(rep)
  return rep.args[0].uint64
 def ThreadSignalCondition(self,condition):
  args=((ValueType.Address,c_uint64,getattr(condition,'value',condition)),)
  rep=self.sndrcv("ThreadSignalCondition",*args)
  self.chk(rep)
 def ThreadTimedWaitForCondition(self,condition,mutex,wait_period_in_ms):
  args=((ValueType.Address,c_uint64,getattr(condition,'value',condition)),
        (ValueType.Address,c_uint64,getattr(mutex,'value',mutex)),
        (ValueType.Scalar,c_int32,wait_period_in_ms),)
  rep=self.sndrcv("ThreadTimedWaitForCondition",*args)
  self.chk(rep)
  return try_cast_to_enum(ConditionAwakeReason, rep.args[0].int32)
 def ThreadWaitForCondition(self,condition,mutex):
  args=((ValueType.Address,c_uint64,getattr(condition,'value',condition)),
        (ValueType.Address,c_uint64,getattr(mutex,'value',mutex)),)
  rep=self.sndrcv("ThreadWaitForCondition",*args)
  self.chk(rep)
 def ThreeDViewGetDistanceToRotateOriginPlane(self):
  rep=self.sndrcv("ThreeDViewGetDistanceToRotateOriginPlane")
  self.chk(rep)
  return rep.args[0].float64
 def ThreeDViewGetMedianAxisRange(self):
  rep=self.sndrcv("ThreeDViewGetMedianAxisRange")
  self.chk(rep)
  return rep.args[0].float64
 def ThreeDViewGetMidZPlane(self):
  rep=self.sndrcv("ThreeDViewGetMidZPlane")
  self.chk(rep)
  return rep.args[0].float64
 def ThreeDViewGetMinMaxPanes(self):
  rep=self.sndrcv("ThreeDViewGetMinMaxPanes")
  self.chk(rep)
  return (
   rep.args[0].float64,
   rep.args[1].float64)
 def ThreeDViewGetNearZPlane(self):
  rep=self.sndrcv("ThreeDViewGetNearZPlane")
  self.chk(rep)
  return rep.args[0].float64
 def ThreeDViewGetProjection(self):
  rep=self.sndrcv("ThreeDViewGetProjection")
  self.chk(rep)
  return (
   rep.args[0].float64,
   rep.args[1].float64,
   rep.args[2].boolean)
 def ThreeDViewGetViewerAngle(self):
  rep=self.sndrcv("ThreeDViewGetViewerAngle")
  self.chk(rep)
  return (
   rep.args[0].float64,
   rep.args[1].float64,
   rep.args[2].float64)
 def ThreeDViewGetViewerPos(self):
  rep=self.sndrcv("ThreeDViewGetViewerPos")
  self.chk(rep)
  return (
   rep.args[0].float64,
   rep.args[1].float64,
   rep.args[2].float64)
 def ThreedViewGetDefaultAngles(self):
  rep=self.sndrcv("ThreedViewGetDefaultAngles")
  self.chk(rep)
  return (
   rep.args[0].float64,
   rep.args[1].float64,
   rep.args[2].float64)
 def ToolbarActivate(self,activate):
  args=((ValueType.Scalar,c_bool,activate),)
  rep=self.sndrcv("ToolbarActivate",*args)
  self.chk(rep)
 def TransformCoordinatesX(self,arg_list):
  args=((ValueType.Address,c_uint64,getattr(arg_list,'value',arg_list)),)
  rep=self.sndrcv("TransformCoordinatesX",*args)
  self.chk(rep)
  return (rep.status == tecrpc.Reply.Success)
 def Triangulate(self,source_zones,do_boundary,boundary_zones,include_boundary_pts,triangle_keep_factor):
  args=((ValueType.Address,c_uint64,getattr(source_zones,'value',source_zones)),
        (ValueType.Scalar,c_bool,do_boundary),
        (ValueType.Address,c_uint64,getattr(boundary_zones,'value',boundary_zones)),
        (ValueType.Scalar,c_bool,include_boundary_pts),
        (ValueType.Scalar,c_double,triangle_keep_factor),)
  rep=self.sndrcv("Triangulate",*args)
  self.chk(rep)
  return (
   (rep.status == tecrpc.Reply.Success),
   rep.args[0].int64)
 def UndoCanUndo(self):
  rep=self.sndrcv("UndoCanUndo")
  self.chk(rep)
  return rep.args[0].boolean
 def UndoDoUndo(self):
  rep=self.sndrcv("UndoDoUndo")
  self.chk(rep)
  return (rep.status == tecrpc.Reply.Success)
 def UndoGetCategoryText(self):
  rep=self.sndrcv("UndoGetCategoryText")
  self.chk(rep)
  return (
   (rep.status == tecrpc.Reply.Success),
   self.read_text(rep.args[0]))
 def UndoStateBegin(self,category):
  args=((ValueType.Scalar,c_int32,UndoStateCategory(category).value),)
  rep=self.sndrcv("UndoStateBegin",*args)
  self.chk(rep)
 def UndoStateEnd(self,do_invalidate,do_commit):
  args=((ValueType.Scalar,c_bool,do_invalidate),
        (ValueType.Scalar,c_bool,do_commit),)
  rep=self.sndrcv("UndoStateEnd",*args)
  self.chk(rep)
 def UninstallProbeCallback(self):
  rep=self.sndrcv("UninstallProbeCallback")
  self.chk(rep)
 def UserMacroIsRecordingActive(self):
  rep=self.sndrcv("UserMacroIsRecordingActive")
  self.chk(rep)
  return rep.args[0].boolean
 def VarGetEnabled(self):
  rep=self.sndrcv("VarGetEnabled")
  self.chk(rep)
  return (
   (rep.status == tecrpc.Reply.Success),
   rep.args[0].uint64)
 def VarGetEnabledByDataSetID(self,data_set_id):
  args=((ValueType.Scalar,c_int64,data_set_id),)
  rep=self.sndrcv("VarGetEnabledByDataSetID",*args)
  self.chk(rep)
  return (
   (rep.status == tecrpc.Reply.Success),
   rep.args[0].uint64)
 def VarGetEnabledForFrame(self,frame_id):
  args=((ValueType.Scalar,c_int64,frame_id),)
  rep=self.sndrcv("VarGetEnabledForFrame",*args)
  self.chk(rep)
  return (
   (rep.status == tecrpc.Reply.Success),
   rep.args[0].uint64)
 def VarGetEnabledNamesByDataSetID(self,data_set_id):
  args=((ValueType.Scalar,c_int64,data_set_id),)
  rep=self.sndrcv("VarGetEnabledNamesByDataSetID",*args)
  self.chk(rep)
  return (
   (rep.status == tecrpc.Reply.Success),
   rep.args[0].uint64)
 def VarGetMinMax(self,var):
  args=((ValueType.Scalar,c_int32,var),)
  rep=self.sndrcv("VarGetMinMax",*args)
  self.chk(rep)
  return (
   (rep.status == tecrpc.Reply.Success),
   rep.args[0].float64,
   rep.args[1].float64)
 def VarGetName(self,var_num):
  args=((ValueType.Scalar,c_int32,var_num),)
  rep=self.sndrcv("VarGetName",*args)
  self.chk(rep)
  return (
   (rep.status == tecrpc.Reply.Success),
   self.read_text(rep.args[0]))
 def VarGetNameByDataSetID(self,data_set_id,var_num):
  args=((ValueType.Scalar,c_int64,data_set_id),
        (ValueType.Scalar,c_int32,var_num),)
  rep=self.sndrcv("VarGetNameByDataSetID",*args)
  self.chk(rep)
  return (
   (rep.status == tecrpc.Reply.Success),
   self.read_text(rep.args[0]))
 def VarGetNameForFrame(self,frame_id,var_num):
  args=((ValueType.Scalar,c_int64,frame_id),
        (ValueType.Scalar,c_int32,var_num),)
  rep=self.sndrcv("VarGetNameForFrame",*args)
  self.chk(rep)
  return (
   (rep.status == tecrpc.Reply.Success),
   self.read_text(rep.args[0]))
 def VarGetNamesByDataSetID(self,data_set_id):
  args=((ValueType.Scalar,c_int64,data_set_id),)
  rep=self.sndrcv("VarGetNamesByDataSetID",*args)
  self.chk(rep)
  return (
   (rep.status == tecrpc.Reply.Success),
   rep.args[0].uint64)
 def VarGetNonBlankedMinMax(self,zone_set,var):
  args=((ValueType.Address,c_uint64,getattr(zone_set,'value',zone_set)),
        (ValueType.Scalar,c_int32,var),)
  rep=self.sndrcv("VarGetNonBlankedMinMax",*args)
  self.chk(rep)
  return (
   (rep.status == tecrpc.Reply.Success),
   rep.args[0].float64,
   rep.args[1].float64)
 def VarGetNumByAssignment(self,var):
  args=((ValueType.Text,None,var),)
  rep=self.sndrcv("VarGetNumByAssignment",*args)
  self.chk(rep)
  return rep.args[0].int32
 def VarGetNumByName(self,var_name):
  args=((ValueType.Text,None,var_name),)
  rep=self.sndrcv("VarGetNumByName",*args)
  self.chk(rep)
  return rep.args[0].int32
 def VarGetNumByUniqueID(self,unique_id):
  args=((ValueType.Scalar,c_int64,unique_id),)
  rep=self.sndrcv("VarGetNumByUniqueID",*args)
  self.chk(rep)
  return rep.args[0].int32
 def VarGetNumFromStyleString(self,var_token,allow_zero):
  args=((ValueType.Text,None,var_token),
        (ValueType.Scalar,c_bool,allow_zero),)
  rep=self.sndrcv("VarGetNumFromStyleString",*args)
  self.chk(rep)
  return (
   try_cast_to_enum(VarParseReturnCode, rep.args[0].int32),
   rep.args[1].int32)
 def VarGetStatus(self,zone,var):
  args=((ValueType.Scalar,c_int32,zone),
        (ValueType.Scalar,c_int32,var),)
  rep=self.sndrcv("VarGetStatus",*args)
  self.chk(rep)
  return try_cast_to_enum(VarStatus, rep.args[0].int32)
 def VarGetStatusByRef(self,field_data):
  args=((ValueType.Address,c_uint64,getattr(field_data,'value',field_data)),)
  rep=self.sndrcv("VarGetStatusByRef",*args)
  self.chk(rep)
  return try_cast_to_enum(VarStatus, rep.args[0].int32)
 def VarGetStyleStringFromNum(self,var_num):
  args=((ValueType.Scalar,c_int32,var_num),)
  rep=self.sndrcv("VarGetStyleStringFromNum",*args)
  self.chk(rep)
  return (
   (rep.status == tecrpc.Reply.Success),
   self.read_text(rep.args[0]))
 def VarGetUniqueID(self,var):
  args=((ValueType.Scalar,c_int32,var),)
  rep=self.sndrcv("VarGetUniqueID",*args)
  self.chk(rep)
  return rep.args[0].int64
 def VarGetUniqueIDByDataSetID(self,data_set_id,var):
  args=((ValueType.Scalar,c_int64,data_set_id),
        (ValueType.Scalar,c_int32,var),)
  rep=self.sndrcv("VarGetUniqueIDByDataSetID",*args)
  self.chk(rep)
  return rep.args[0].int64
 def VarGetUniqueIDForFrame(self,frame_id,var):
  args=((ValueType.Scalar,c_int64,frame_id),
        (ValueType.Scalar,c_int32,var),)
  rep=self.sndrcv("VarGetUniqueIDForFrame",*args)
  self.chk(rep)
  return rep.args[0].int64
 def VarGetUniqueIDsByDataSetID(self,data_set_id):
  args=((ValueType.Scalar,c_int64,data_set_id),)
  rep=self.sndrcv("VarGetUniqueIDsByDataSetID",*args)
  self.chk(rep)
  return (
   (rep.status == tecrpc.Reply.Success),
   len(rep.args[0].buffer)//sizeof(c_int64),
   self.read_array(rep.args[0], c_int64))
 def VarIsEnabled(self,var):
  args=((ValueType.Scalar,c_int32,var),)
  rep=self.sndrcv("VarIsEnabled",*args)
  self.chk(rep)
  return rep.args[0].boolean
 def VarIsEnabledByDataSetID(self,data_set_id,var):
  args=((ValueType.Scalar,c_int64,data_set_id),
        (ValueType.Scalar,c_int32,var),)
  rep=self.sndrcv("VarIsEnabledByDataSetID",*args)
  self.chk(rep)
  return rep.args[0].boolean
 def VarIsEnabledForFrame(self,frame_id,var):
  args=((ValueType.Scalar,c_int64,frame_id),
        (ValueType.Scalar,c_int32,var),)
  rep=self.sndrcv("VarIsEnabledForFrame",*args)
  self.chk(rep)
  return rep.args[0].boolean
 def VarIsSZLData(self,zone,var):
  args=((ValueType.Scalar,c_int32,zone),
        (ValueType.Scalar,c_int32,var),)
  rep=self.sndrcv("VarIsSZLData",*args)
  self.chk(rep)
  return rep.args[0].boolean
 def VarIsSpatial(self,var):
  args=((ValueType.Scalar,c_int32,var),)
  rep=self.sndrcv("VarIsSpatial",*args)
  self.chk(rep)
  return rep.args[0].boolean
 def VarIsSpatialForFrame(self,frame_id,var):
  args=((ValueType.Scalar,c_int64,frame_id),
        (ValueType.Scalar,c_int32,var),)
  rep=self.sndrcv("VarIsSpatialForFrame",*args)
  self.chk(rep)
  return rep.args[0].boolean
 def VarRangeIsEstimated(self,zone,var):
  args=((ValueType.Scalar,c_int32,zone),
        (ValueType.Scalar,c_int32,var),)
  rep=self.sndrcv("VarRangeIsEstimated",*args)
  self.chk(rep)
  return rep.args[0].boolean
 def VarRename(self,var_num,var_name):
  args=((ValueType.Scalar,c_int32,var_num),
        (ValueType.Text,None,var_name),)
  rep=self.sndrcv("VarRename",*args)
  self.chk(rep)
  return (rep.status == tecrpc.Reply.Success)
 def VarRenameByDataSetID(self,data_set_id,var_num,var_name):
  args=((ValueType.Scalar,c_int64,data_set_id),
        (ValueType.Scalar,c_int32,var_num),
        (ValueType.Text,None,var_name),)
  rep=self.sndrcv("VarRenameByDataSetID",*args)
  self.chk(rep)
  return (rep.status == tecrpc.Reply.Success)
 def VarRenameForFrame(self,frame_id,var_num,var_name):
  args=((ValueType.Scalar,c_int64,frame_id),
        (ValueType.Scalar,c_int32,var_num),
        (ValueType.Text,None,var_name),)
  rep=self.sndrcv("VarRenameForFrame",*args)
  self.chk(rep)
  return (rep.status == tecrpc.Reply.Success)
 def VariableIsLocked(self,var):
  args=((ValueType.Scalar,c_int32,var),)
  rep=self.sndrcv("VariableIsLocked",*args)
  self.chk(rep)
  return (
   rep.args[0].boolean,
   try_cast_to_enum(VarLockMode, rep.args[1].int32),
   self.read_text(rep.args[2]))
 def VariableLockOff(self,var,lock_owner):
  args=((ValueType.Scalar,c_int32,var),
        (ValueType.Text,None,lock_owner),)
  rep=self.sndrcv("VariableLockOff",*args)
  self.chk(rep)
  return (rep.status == tecrpc.Reply.Success)
 def VariableLockOn(self,var,var_lock_mode,lock_owner):
  args=((ValueType.Scalar,c_int32,var),
        (ValueType.Scalar,c_int32,VarLockMode(var_lock_mode).value),
        (ValueType.Text,None,lock_owner),)
  rep=self.sndrcv("VariableLockOn",*args)
  self.chk(rep)
  return (rep.status == tecrpc.Reply.Success)
 def VectorCheckVariableAssignments(self):
  rep=self.sndrcv("VectorCheckVariableAssignments")
  self.chk(rep)
  return rep.args[0].boolean
 def ViewAxisFit(self,axis,axis_num):
  args=((ValueType.Text,None,axis),
        (ValueType.Scalar,c_int32,axis_num),)
  rep=self.sndrcv("ViewAxisFit",*args)
  self.chk(rep)
  return (rep.status == tecrpc.Reply.Success)
 def ViewAxisFitToEntireCircle(self,axis,axis_num):
  args=((ValueType.Text,None,axis),
        (ValueType.Scalar,c_int32,axis_num),)
  rep=self.sndrcv("ViewAxisFitToEntireCircle",*args)
  self.chk(rep)
  return (rep.status == tecrpc.Reply.Success)
 def ViewAxisMakeCurValsNice(self,axis,axis_num):
  args=((ValueType.Text,None,axis),
        (ValueType.Scalar,c_int32,axis_num),)
  rep=self.sndrcv("ViewAxisMakeCurValsNice",*args)
  self.chk(rep)
  return (rep.status == tecrpc.Reply.Success)
 def ViewAxisNiceFit(self,axis,axis_num):
  args=((ValueType.Text,None,axis),
        (ValueType.Scalar,c_int32,axis_num),)
  rep=self.sndrcv("ViewAxisNiceFit",*args)
  self.chk(rep)
  return (rep.status == tecrpc.Reply.Success)
 def ViewCenter(self):
  rep=self.sndrcv("ViewCenter")
  self.chk(rep)
  return (rep.status == tecrpc.Reply.Success)
 def ViewCopy(self):
  rep=self.sndrcv("ViewCopy")
  self.chk(rep)
  return (rep.status == tecrpc.Reply.Success)
 def ViewDataFit(self):
  rep=self.sndrcv("ViewDataFit")
  self.chk(rep)
  return (rep.status == tecrpc.Reply.Success)
 def ViewDealloc(self,view_state):
  args=((ValueType.Address,c_uint64,view_state.contents.value),)
  rep=self.sndrcv("ViewDealloc",*args)
  self.chk(rep)
  return rep.args[0].uint64
 def ViewFit(self):
  rep=self.sndrcv("ViewFit")
  self.chk(rep)
  return (rep.status == tecrpc.Reply.Success)
 def ViewFitSurfaces(self):
  rep=self.sndrcv("ViewFitSurfaces")
  self.chk(rep)
  return (rep.status == tecrpc.Reply.Success)
 def ViewGet(self):
  rep=self.sndrcv("ViewGet")
  self.chk(rep)
  return rep.args[0].uint64
 def ViewGetMagnification(self):
  rep=self.sndrcv("ViewGetMagnification")
  self.chk(rep)
  return (
   (rep.status == tecrpc.Reply.Success),
   rep.args[0].float64)
 def ViewGetPlotType(self,view_state):
  args=((ValueType.Address,c_uint64,getattr(view_state,'value',view_state)),)
  rep=self.sndrcv("ViewGetPlotType",*args)
  self.chk(rep)
  return try_cast_to_enum(PlotType, rep.args[0].int32)
 def ViewLast(self):
  rep=self.sndrcv("ViewLast")
  self.chk(rep)
  return (rep.status == tecrpc.Reply.Success)
 def ViewMakeCurViewNice(self):
  rep=self.sndrcv("ViewMakeCurViewNice")
  self.chk(rep)
  return (rep.status == tecrpc.Reply.Success)
 def ViewNiceFit(self):
  rep=self.sndrcv("ViewNiceFit")
  self.chk(rep)
  return (rep.status == tecrpc.Reply.Success)
 def ViewOkToPaste(self):
  rep=self.sndrcv("ViewOkToPaste")
  self.chk(rep)
  return rep.args[0].boolean
 def ViewPaste(self):
  rep=self.sndrcv("ViewPaste")
  self.chk(rep)
  return (rep.status == tecrpc.Reply.Success)
 def ViewPush(self):
  rep=self.sndrcv("ViewPush")
  self.chk(rep)
  return (rep.status == tecrpc.Reply.Success)
 def ViewRotate3D(self,rotate_axis,rotate_amount_in_degrees,vector_x,vector_y,vector_z,rotate_origin_location):
  args=((ValueType.Scalar,c_int32,RotateAxis(rotate_axis).value),
        (ValueType.Scalar,c_double,rotate_amount_in_degrees),
        (ValueType.Scalar,c_double,vector_x),
        (ValueType.Scalar,c_double,vector_y),
        (ValueType.Scalar,c_double,vector_z),
        (ValueType.Scalar,c_int32,RotateOriginLocation(rotate_origin_location).value),)
  rep=self.sndrcv("ViewRotate3D",*args)
  self.chk(rep)
  return (rep.status == tecrpc.Reply.Success)
 def ViewSet(self,view_state):
  args=((ValueType.Address,c_uint64,getattr(view_state,'value',view_state)),)
  rep=self.sndrcv("ViewSet",*args)
  self.chk(rep)
  return (rep.status == tecrpc.Reply.Success)
 def ViewSetMagnification(self,magnification):
  args=((ValueType.Scalar,c_double,magnification),)
  rep=self.sndrcv("ViewSetMagnification",*args)
  self.chk(rep)
  return (rep.status == tecrpc.Reply.Success)
 def ViewTranslate(self,x,y):
  args=((ValueType.Scalar,c_double,x),
        (ValueType.Scalar,c_double,y),)
  rep=self.sndrcv("ViewTranslate",*args)
  self.chk(rep)
  return (rep.status == tecrpc.Reply.Success)
 def ViewX(self,arg_list):
  args=((ValueType.Address,c_uint64,getattr(arg_list,'value',arg_list)),)
  rep=self.sndrcv("ViewX",*args)
  self.chk(rep)
  return (rep.status == tecrpc.Reply.Success)
 def ViewZoom(self,x1,y1,x2,y2):
  args=((ValueType.Scalar,c_double,x1),
        (ValueType.Scalar,c_double,y1),
        (ValueType.Scalar,c_double,x2),
        (ValueType.Scalar,c_double,y2),)
  rep=self.sndrcv("ViewZoom",*args)
  self.chk(rep)
  return (rep.status == tecrpc.Reply.Success)
 def WinCopyToClipboard(self):
  rep=self.sndrcv("WinCopyToClipboard")
  self.chk(rep)
  return (rep.status == tecrpc.Reply.Success)
 def WorkAreaGetDimensions(self):
  rep=self.sndrcv("WorkAreaGetDimensions")
  self.chk(rep)
  return (
   rep.args[0].int32,
   rep.args[1].int32)
 def WorkAreaSuspend(self,do_suspend):
  args=((ValueType.Scalar,c_bool,do_suspend),)
  rep=self.sndrcv("WorkAreaSuspend",*args)
  self.chk(rep)
 def WorkViewFitAllFrames(self):
  rep=self.sndrcv("WorkViewFitAllFrames")
  self.chk(rep)
  return (rep.status == tecrpc.Reply.Success)
 def WorkViewFitPaper(self):
  rep=self.sndrcv("WorkViewFitPaper")
  self.chk(rep)
  return (rep.status == tecrpc.Reply.Success)
 def WorkViewFitSelectFrames(self):
  rep=self.sndrcv("WorkViewFitSelectFrames")
  self.chk(rep)
  return (rep.status == tecrpc.Reply.Success)
 def WorkViewLastView(self):
  rep=self.sndrcv("WorkViewLastView")
  self.chk(rep)
  return (rep.status == tecrpc.Reply.Success)
 def WorkViewMaximize(self):
  rep=self.sndrcv("WorkViewMaximize")
  self.chk(rep)
  return (rep.status == tecrpc.Reply.Success)
 def WorkViewTranslate(self,x,y):
  args=((ValueType.Scalar,c_double,x),
        (ValueType.Scalar,c_double,y),)
  rep=self.sndrcv("WorkViewTranslate",*args)
  self.chk(rep)
  return (rep.status == tecrpc.Reply.Success)
 def WorkViewZoom(self,x1,y1,x2,y2):
  args=((ValueType.Scalar,c_double,x1),
        (ValueType.Scalar,c_double,y1),
        (ValueType.Scalar,c_double,x2),
        (ValueType.Scalar,c_double,y2),)
  rep=self.sndrcv("WorkViewZoom",*args)
  self.chk(rep)
  return (rep.status == tecrpc.Reply.Success)
 def WriteColorMap(self,f_name):
  args=((ValueType.Text,None,f_name),)
  rep=self.sndrcv("WriteColorMap",*args)
  self.chk(rep)
  return (rep.status == tecrpc.Reply.Success)
 def WriteDataSet(self,f_name,include_text,include_geom,include_custom_labels,include_data,zones_to_write,vars_to_write,write_binary,use_point_format,ascii_precision):
  args=((ValueType.Text,None,f_name),
        (ValueType.Scalar,c_bool,include_text),
        (ValueType.Scalar,c_bool,include_geom),
        (ValueType.Scalar,c_bool,include_custom_labels),
        (ValueType.Scalar,c_bool,include_data),
        (ValueType.Address,c_uint64,getattr(zones_to_write,'value',zones_to_write)),
        (ValueType.Address,c_uint64,getattr(vars_to_write,'value',vars_to_write)),
        (ValueType.Scalar,c_bool,write_binary),
        (ValueType.Scalar,c_bool,use_point_format),
        (ValueType.Scalar,c_int32,ascii_precision),)
  rep=self.sndrcv("WriteDataSet",*args)
  self.chk(rep)
  return (rep.status == tecrpc.Reply.Success)
 def WriteStylesheet(self,f_name,include_plot_style,include_text,include_geom,include_stream_positions,include_contour_levels,include_factory_defaults):
  args=((ValueType.Text,None,f_name),
        (ValueType.Scalar,c_bool,include_plot_style),
        (ValueType.Scalar,c_bool,include_text),
        (ValueType.Scalar,c_bool,include_geom),
        (ValueType.Scalar,c_bool,include_stream_positions),
        (ValueType.Scalar,c_bool,include_contour_levels),
        (ValueType.Scalar,c_bool,include_factory_defaults),)
  rep=self.sndrcv("WriteStylesheet",*args)
  self.chk(rep)
  return (rep.status == tecrpc.Reply.Success)
 def WriteStylesheetX(self,arg_list):
  args=((ValueType.Address,c_uint64,getattr(arg_list,'value',arg_list)),)
  rep=self.sndrcv("WriteStylesheetX",*args)
  self.chk(rep)
  return (rep.status == tecrpc.Reply.Success)
 def ZoneCopy(self,zone_used,i_min,i_max,i_skip,j_min,j_max,j_skip,k_min,k_max,k_skip):
  args=((ValueType.Scalar,c_int32,zone_used),
        (ValueType.Scalar,c_int64,i_min),
        (ValueType.Scalar,c_int64,i_max),
        (ValueType.Scalar,c_int64,i_skip),
        (ValueType.Scalar,c_int64,j_min),
        (ValueType.Scalar,c_int64,j_max),
        (ValueType.Scalar,c_int64,j_skip),
        (ValueType.Scalar,c_int64,k_min),
        (ValueType.Scalar,c_int64,k_max),
        (ValueType.Scalar,c_int64,k_skip),)
  rep=self.sndrcv("ZoneCopy",*args)
  self.chk(rep)
  return (rep.status == tecrpc.Reply.Success)
 def ZoneCopyX(self,arg_list):
  args=((ValueType.Address,c_uint64,getattr(arg_list,'value',arg_list)),)
  rep=self.sndrcv("ZoneCopyX",*args)
  self.chk(rep)
  return (rep.status == tecrpc.Reply.Success)
 def ZoneGetActive(self):
  rep=self.sndrcv("ZoneGetActive")
  self.chk(rep)
  return (
   (rep.status == tecrpc.Reply.Success),
   rep.args[0].uint64)
 def ZoneGetActiveForFrame(self,frame_id):
  args=((ValueType.Scalar,c_int64,frame_id),)
  rep=self.sndrcv("ZoneGetActiveForFrame",*args)
  self.chk(rep)
  return (
   (rep.status == tecrpc.Reply.Success),
   rep.args[0].uint64)
 def ZoneGetEnabled(self):
  rep=self.sndrcv("ZoneGetEnabled")
  self.chk(rep)
  return (
   (rep.status == tecrpc.Reply.Success),
   rep.args[0].uint64)
 def ZoneGetEnabledByDataSetID(self,data_set_id):
  args=((ValueType.Scalar,c_int64,data_set_id),)
  rep=self.sndrcv("ZoneGetEnabledByDataSetID",*args)
  self.chk(rep)
  return (
   (rep.status == tecrpc.Reply.Success),
   rep.args[0].uint64)
 def ZoneGetEnabledForFrame(self,frame_id):
  args=((ValueType.Scalar,c_int64,frame_id),)
  rep=self.sndrcv("ZoneGetEnabledForFrame",*args)
  self.chk(rep)
  return (
   (rep.status == tecrpc.Reply.Success),
   rep.args[0].uint64)
 def ZoneGetEnabledNamesByDataSetID(self,data_set_id):
  args=((ValueType.Scalar,c_int64,data_set_id),)
  rep=self.sndrcv("ZoneGetEnabledNamesByDataSetID",*args)
  self.chk(rep)
  return (
   (rep.status == tecrpc.Reply.Success),
   rep.args[0].uint64)
 def ZoneGetFieldMap(self,zone):
  args=((ValueType.Scalar,c_int32,zone),)
  rep=self.sndrcv("ZoneGetFieldMap",*args)
  self.chk(rep)
  return rep.args[0].int32
 def ZoneGetIJK(self,cur_zone):
  args=((ValueType.Scalar,c_int32,cur_zone),)
  rep=self.sndrcv("ZoneGetIJK",*args)
  self.chk(rep)
  return (
   rep.args[0].int64,
   rep.args[1].int64,
   rep.args[2].int64)
 def ZoneGetIJKByUniqueID(self,dataset_id,zone):
  args=((ValueType.Scalar,c_int64,dataset_id),
        (ValueType.Scalar,c_int32,zone),)
  rep=self.sndrcv("ZoneGetIJKByUniqueID",*args)
  self.chk(rep)
  return (
   rep.args[0].int64,
   rep.args[1].int64,
   rep.args[2].int64)
 def ZoneGetInfo(self,cur_zone):
  args=((ValueType.Scalar,c_int32,cur_zone),)
  rep=self.sndrcv("ZoneGetInfo",*args)
  self.chk(rep)
  return (
   rep.args[0].int64,
   rep.args[1].int64,
   rep.args[2].int64,
   rep.args[3].uint64,
   rep.args[4].uint64,
   rep.args[5].uint64,
   rep.args[6].uint64,
   rep.args[7].uint64,
   rep.args[8].uint64,
   rep.args[9].uint64,
   rep.args[10].uint64,
   rep.args[11].uint64,
   rep.args[12].uint64)
 def ZoneGetInfoForFrame(self,frame_id,cur_zone):
  args=((ValueType.Scalar,c_int64,frame_id),
        (ValueType.Scalar,c_int32,cur_zone),)
  rep=self.sndrcv("ZoneGetInfoForFrame",*args)
  self.chk(rep)
  return (
   rep.args[0].int64,
   rep.args[1].int64,
   rep.args[2].int64,
   rep.args[3].uint64,
   rep.args[4].uint64,
   rep.args[5].uint64,
   rep.args[6].uint64,
   rep.args[7].uint64,
   rep.args[8].uint64,
   rep.args[9].uint64,
   rep.args[10].uint64,
   rep.args[11].uint64,
   rep.args[12].uint64)
 def ZoneGetName(self,zone):
  args=((ValueType.Scalar,c_int32,zone),)
  rep=self.sndrcv("ZoneGetName",*args)
  self.chk(rep)
  return (
   (rep.status == tecrpc.Reply.Success),
   self.read_text(rep.args[0]))
 def ZoneGetNameByDataSetID(self,data_set_id,zone):
  args=((ValueType.Scalar,c_int64,data_set_id),
        (ValueType.Scalar,c_int32,zone),)
  rep=self.sndrcv("ZoneGetNameByDataSetID",*args)
  self.chk(rep)
  return (
   (rep.status == tecrpc.Reply.Success),
   self.read_text(rep.args[0]))
 def ZoneGetNameForFrame(self,frame_id,zone):
  args=((ValueType.Scalar,c_int64,frame_id),
        (ValueType.Scalar,c_int32,zone),)
  rep=self.sndrcv("ZoneGetNameForFrame",*args)
  self.chk(rep)
  return (
   (rep.status == tecrpc.Reply.Success),
   self.read_text(rep.args[0]))
 def ZoneGetNamesByDataSetID(self,data_set_id):
  args=((ValueType.Scalar,c_int64,data_set_id),)
  rep=self.sndrcv("ZoneGetNamesByDataSetID",*args)
  self.chk(rep)
  return (
   (rep.status == tecrpc.Reply.Success),
   rep.args[0].uint64)
 def ZoneGetNumByUniqueID(self,unique_id):
  args=((ValueType.Scalar,c_int64,unique_id),)
  rep=self.sndrcv("ZoneGetNumByUniqueID",*args)
  self.chk(rep)
  return rep.args[0].int32
 def ZoneGetSolutionTime(self,zone):
  args=((ValueType.Scalar,c_int32,zone),)
  rep=self.sndrcv("ZoneGetSolutionTime",*args)
  self.chk(rep)
  return rep.args[0].float64
 def ZoneGetStrandID(self,zone):
  args=((ValueType.Scalar,c_int32,zone),)
  rep=self.sndrcv("ZoneGetStrandID",*args)
  self.chk(rep)
  return rep.args[0].int32
 def ZoneGetStrandIDByDataSetID(self,data_set_id,zone):
  args=((ValueType.Scalar,c_int64,data_set_id),
        (ValueType.Scalar,c_int32,zone),)
  rep=self.sndrcv("ZoneGetStrandIDByDataSetID",*args)
  self.chk(rep)
  return rep.args[0].int32
 def ZoneGetType(self,zone):
  args=((ValueType.Scalar,c_int32,zone),)
  rep=self.sndrcv("ZoneGetType",*args)
  self.chk(rep)
  return try_cast_to_enum(ZoneType, rep.args[0].int32)
 def ZoneGetTypeByDataSetID(self,data_set_id,zone):
  args=((ValueType.Scalar,c_int64,data_set_id),
        (ValueType.Scalar,c_int32,zone),)
  rep=self.sndrcv("ZoneGetTypeByDataSetID",*args)
  self.chk(rep)
  return try_cast_to_enum(ZoneType, rep.args[0].int32)
 def ZoneGetTypesByDataSetID(self,data_set_id):
  args=((ValueType.Scalar,c_int64,data_set_id),)
  rep=self.sndrcv("ZoneGetTypesByDataSetID",*args)
  self.chk(rep)
  return (
   (rep.status == tecrpc.Reply.Success),
   len(rep.args[0].buffer)//sizeof(c_int32),
   self.read_enum_array(rep.args[0], ZoneType))
 def ZoneGetUniqueID(self,zone):
  args=((ValueType.Scalar,c_int32,zone),)
  rep=self.sndrcv("ZoneGetUniqueID",*args)
  self.chk(rep)
  return rep.args[0].int64
 def ZoneGetUniqueIDByDataSetID(self,data_set_id,zone):
  args=((ValueType.Scalar,c_int64,data_set_id),
        (ValueType.Scalar,c_int32,zone),)
  rep=self.sndrcv("ZoneGetUniqueIDByDataSetID",*args)
  self.chk(rep)
  return rep.args[0].int64
 def ZoneGetUniqueIDForFrame(self,frame_id,zone):
  args=((ValueType.Scalar,c_int64,frame_id),
        (ValueType.Scalar,c_int32,zone),)
  rep=self.sndrcv("ZoneGetUniqueIDForFrame",*args)
  self.chk(rep)
  return rep.args[0].int64
 def ZoneGetUniqueIDsByDataSetID(self,data_set_id):
  args=((ValueType.Scalar,c_int64,data_set_id),)
  rep=self.sndrcv("ZoneGetUniqueIDsByDataSetID",*args)
  self.chk(rep)
  return (
   (rep.status == tecrpc.Reply.Success),
   len(rep.args[0].buffer)//sizeof(c_int64),
   self.read_array(rep.args[0], c_int64))
 def ZoneIsActive(self,zone):
  args=((ValueType.Scalar,c_int32,zone),)
  rep=self.sndrcv("ZoneIsActive",*args)
  self.chk(rep)
  return rep.args[0].boolean
 def ZoneIsActiveForFrame(self,frame_id,zone):
  args=((ValueType.Scalar,c_int64,frame_id),
        (ValueType.Scalar,c_int32,zone),)
  rep=self.sndrcv("ZoneIsActiveForFrame",*args)
  self.chk(rep)
  return rep.args[0].boolean
 def ZoneIsEnabled(self,zone):
  args=((ValueType.Scalar,c_int32,zone),)
  rep=self.sndrcv("ZoneIsEnabled",*args)
  self.chk(rep)
  return rep.args[0].boolean
 def ZoneIsEnabledByDataSetID(self,data_set_id,zone):
  args=((ValueType.Scalar,c_int64,data_set_id),
        (ValueType.Scalar,c_int32,zone),)
  rep=self.sndrcv("ZoneIsEnabledByDataSetID",*args)
  self.chk(rep)
  return rep.args[0].boolean
 def ZoneIsFEClassic(self,zone):
  args=((ValueType.Scalar,c_int32,zone),)
  rep=self.sndrcv("ZoneIsFEClassic",*args)
  self.chk(rep)
  return rep.args[0].boolean
 def ZoneIsFEPolytope(self,zone):
  args=((ValueType.Scalar,c_int32,zone),)
  rep=self.sndrcv("ZoneIsFEPolytope",*args)
  self.chk(rep)
  return rep.args[0].boolean
 def ZoneIsFiniteElement(self,zone):
  args=((ValueType.Scalar,c_int32,zone),)
  rep=self.sndrcv("ZoneIsFiniteElement",*args)
  self.chk(rep)
  return rep.args[0].boolean
 def ZoneIsLinear(self,zone):
  args=((ValueType.Scalar,c_int32,zone),)
  rep=self.sndrcv("ZoneIsLinear",*args)
  self.chk(rep)
  return rep.args[0].boolean
 def ZoneIsLinearByDataSetID(self,data_set_id,zone):
  args=((ValueType.Scalar,c_int64,data_set_id),
        (ValueType.Scalar,c_int32,zone),)
  rep=self.sndrcv("ZoneIsLinearByDataSetID",*args)
  self.chk(rep)
  return rep.args[0].boolean
 def ZoneIsLinearForFrame(self,frame_id,zone):
  args=((ValueType.Scalar,c_int64,frame_id),
        (ValueType.Scalar,c_int32,zone),)
  rep=self.sndrcv("ZoneIsLinearForFrame",*args)
  self.chk(rep)
  return rep.args[0].boolean
 def ZoneIsOrdered(self,zone):
  args=((ValueType.Scalar,c_int32,zone),)
  rep=self.sndrcv("ZoneIsOrdered",*args)
  self.chk(rep)
  return rep.args[0].boolean
 def ZoneIsOrderedByDataSetID(self,data_set_id,zone):
  args=((ValueType.Scalar,c_int64,data_set_id),
        (ValueType.Scalar,c_int32,zone),)
  rep=self.sndrcv("ZoneIsOrderedByDataSetID",*args)
  self.chk(rep)
  return rep.args[0].boolean
 def ZoneIsOrderedForFrame(self,frame_id,zone):
  args=((ValueType.Scalar,c_int64,frame_id),
        (ValueType.Scalar,c_int32,zone),)
  rep=self.sndrcv("ZoneIsOrderedForFrame",*args)
  self.chk(rep)
  return rep.args[0].boolean
 def ZoneIsSZL(self,zone):
  args=((ValueType.Scalar,c_int32,zone),)
  rep=self.sndrcv("ZoneIsSZL",*args)
  self.chk(rep)
  return rep.args[0].boolean
 def ZoneRealloc(self,zone,new_i_max_or_num_data_points,new_j_max_or_num_elements,new_k_max):
  args=((ValueType.Scalar,c_int32,zone),
        (ValueType.Scalar,c_int64,new_i_max_or_num_data_points),
        (ValueType.Scalar,c_int64,new_j_max_or_num_elements),
        (ValueType.Scalar,c_int64,new_k_max),)
  rep=self.sndrcv("ZoneRealloc",*args)
  self.chk(rep)
  return (rep.status == tecrpc.Reply.Success)
 def ZoneRename(self,zone,zone_name):
  args=((ValueType.Scalar,c_int32,zone),
        (ValueType.Text,None,zone_name),)
  rep=self.sndrcv("ZoneRename",*args)
  self.chk(rep)
  return (rep.status == tecrpc.Reply.Success)
 def ZoneRenameByDataSetID(self,data_set_id,zone,zone_name):
  args=((ValueType.Scalar,c_int64,data_set_id),
        (ValueType.Scalar,c_int32,zone),
        (ValueType.Text,None,zone_name),)
  rep=self.sndrcv("ZoneRenameByDataSetID",*args)
  self.chk(rep)
  return (rep.status == tecrpc.Reply.Success)
 def ZoneRenameForFrame(self,frame_id,zone,zone_name):
  args=((ValueType.Scalar,c_int64,frame_id),
        (ValueType.Scalar,c_int32,zone),
        (ValueType.Text,None,zone_name),)
  rep=self.sndrcv("ZoneRenameForFrame",*args)
  self.chk(rep)
  return (rep.status == tecrpc.Reply.Success)
 def ZoneSetActive(self,zone_set,assign_modifier):
  args=((ValueType.Address,c_uint64,getattr(zone_set,'value',zone_set)),
        (ValueType.Scalar,c_int32,AssignOp(assign_modifier).value),)
  rep=self.sndrcv("ZoneSetActive",*args)
  self.chk(rep)
  return try_cast_to_enum(SetValueReturnCode, rep.args[0].int32)
 def ZoneSetBuildZoneOptInfo(self,zone,build_zone_opt_info):
  args=((ValueType.Scalar,c_int32,zone),
        (ValueType.Scalar,c_bool,build_zone_opt_info),)
  rep=self.sndrcv("ZoneSetBuildZoneOptInfo",*args)
  self.chk(rep)
 def ZoneSetContour(self,attribute,zone_set,d_value,i_value):
  args=((ValueType.Text,None,attribute),
        (ValueType.Address,c_uint64,getattr(zone_set,'value',zone_set)),
        (ValueType.Scalar,c_double,d_value),
        (ValueType.ArbParam,None,i_value),)
  rep=self.sndrcv("ZoneSetContour",*args)
  self.chk(rep)
  return try_cast_to_enum(SetValueReturnCode, rep.args[0].int32)
 def ZoneSetEdgeLayer(self,attribute,zone_set,d_value,i_value):
  args=((ValueType.Text,None,attribute),
        (ValueType.Address,c_uint64,getattr(zone_set,'value',zone_set)),
        (ValueType.Scalar,c_double,d_value),
        (ValueType.ArbParam,None,i_value),)
  rep=self.sndrcv("ZoneSetEdgeLayer",*args)
  self.chk(rep)
  return try_cast_to_enum(SetValueReturnCode, rep.args[0].int32)
 def ZoneSetMesh(self,attribute,zone_set,d_value,i_value):
  args=((ValueType.Text,None,attribute),
        (ValueType.Address,c_uint64,getattr(zone_set,'value',zone_set)),
        (ValueType.Scalar,c_double,d_value),
        (ValueType.ArbParam,None,i_value),)
  rep=self.sndrcv("ZoneSetMesh",*args)
  self.chk(rep)
  return try_cast_to_enum(SetValueReturnCode, rep.args[0].int32)
 def ZoneSetScatter(self,attribute,zone_set,d_value,i_value):
  args=((ValueType.Text,None,attribute),
        (ValueType.Address,c_uint64,getattr(zone_set,'value',zone_set)),
        (ValueType.Scalar,c_double,d_value),
        (ValueType.ArbParam,None,i_value),)
  rep=self.sndrcv("ZoneSetScatter",*args)
  self.chk(rep)
  return try_cast_to_enum(SetValueReturnCode, rep.args[0].int32)
 def ZoneSetScatterIJKSkip(self,attribute,zone_set,skip):
  args=((ValueType.Text,None,attribute),
        (ValueType.Address,c_uint64,getattr(zone_set,'value',zone_set)),
        (ValueType.Scalar,c_int64,skip),)
  rep=self.sndrcv("ZoneSetScatterIJKSkip",*args)
  self.chk(rep)
  return try_cast_to_enum(SetValueReturnCode, rep.args[0].int32)
 def ZoneSetScatterSymbolShape(self,attribute,zone_set,i_value):
  args=((ValueType.Text,None,attribute),
        (ValueType.Address,c_uint64,getattr(zone_set,'value',zone_set)),
        (ValueType.ArbParam,None,i_value),)
  rep=self.sndrcv("ZoneSetScatterSymbolShape",*args)
  self.chk(rep)
  return try_cast_to_enum(SetValueReturnCode, rep.args[0].int32)
 def ZoneSetShade(self,attribute,zone_set,d_value,i_value):
  args=((ValueType.Text,None,attribute),
        (ValueType.Address,c_uint64,getattr(zone_set,'value',zone_set)),
        (ValueType.Scalar,c_double,d_value),
        (ValueType.ArbParam,None,i_value),)
  rep=self.sndrcv("ZoneSetShade",*args)
  self.chk(rep)
  return try_cast_to_enum(SetValueReturnCode, rep.args[0].int32)
 def ZoneSetSolutionTime(self,zone,solution_time):
  args=((ValueType.Scalar,c_int32,zone),
        (ValueType.Scalar,c_double,solution_time),)
  rep=self.sndrcv("ZoneSetSolutionTime",*args)
  self.chk(rep)
  return try_cast_to_enum(SetValueReturnCode, rep.args[0].int32)
 def ZoneSetStrandID(self,zone,strand_id):
  args=((ValueType.Scalar,c_int32,zone),
        (ValueType.Scalar,c_int32,strand_id),)
  rep=self.sndrcv("ZoneSetStrandID",*args)
  self.chk(rep)
  return try_cast_to_enum(SetValueReturnCode, rep.args[0].int32)
 def ZoneSetStrandIDByDataSetID(self,data_set_id,zone,strand_id):
  args=((ValueType.Scalar,c_int64,data_set_id),
        (ValueType.Scalar,c_int32,zone),
        (ValueType.Scalar,c_int32,strand_id),)
  rep=self.sndrcv("ZoneSetStrandIDByDataSetID",*args)
  self.chk(rep)
  return try_cast_to_enum(SetValueReturnCode, rep.args[0].int32)
 def ZoneSetVector(self,attribute,zone_set,d_value,i_value):
  args=((ValueType.Text,None,attribute),
        (ValueType.Address,c_uint64,getattr(zone_set,'value',zone_set)),
        (ValueType.Scalar,c_double,d_value),
        (ValueType.ArbParam,None,i_value),)
  rep=self.sndrcv("ZoneSetVector",*args)
  self.chk(rep)
  return try_cast_to_enum(SetValueReturnCode, rep.args[0].int32)
 def ZoneSetVectorIJKSkip(self,attribute,zone_set,skip):
  args=((ValueType.Text,None,attribute),
        (ValueType.Address,c_uint64,getattr(zone_set,'value',zone_set)),
        (ValueType.Scalar,c_int64,skip),)
  rep=self.sndrcv("ZoneSetVectorIJKSkip",*args)
  self.chk(rep)
  return try_cast_to_enum(SetValueReturnCode, rep.args[0].int32)
 def ZoneSetVolumeMode(self,attribute,sub_attribute,zone_set,i_value):
  args=((ValueType.Text,None,attribute),
        (ValueType.Text,None,sub_attribute),
        (ValueType.Address,c_uint64,getattr(zone_set,'value',zone_set)),
        (ValueType.ArbParam,None,i_value),)
  rep=self.sndrcv("ZoneSetVolumeMode",*args)
  self.chk(rep)
  return try_cast_to_enum(SetValueReturnCode, rep.args[0].int32)
 def ZoneSolutionTimeModificationBegin(self):
  rep=self.sndrcv("ZoneSolutionTimeModificationBegin")
  self.chk(rep)
 def ZoneSolutionTimeModificationEnd(self):
  rep=self.sndrcv("ZoneSolutionTimeModificationEnd")
  self.chk(rep)
 def ZoneStyleApplyAuto(self,zone_set):
  args=((ValueType.Address,c_uint64,getattr(zone_set,'value',zone_set)),)
  rep=self.sndrcv("ZoneStyleApplyAuto",*args)
  self.chk(rep)