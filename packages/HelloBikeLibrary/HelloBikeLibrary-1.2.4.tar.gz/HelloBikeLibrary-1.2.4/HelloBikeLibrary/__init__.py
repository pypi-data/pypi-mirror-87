# -*- coding: utf-8 -*-
# @Author: yongfanmao
# @Date:   2020-03-08 13:24:25
# @E-mail: maoyongfan@163.com
# @Last Modified by:   yongfanmao
# @Last Modified time: 2020-12-02 21:33:24

from HelloBikeLibrary.request import Request
from HelloBikeLibrary.version import VERSION
from HelloBikeLibrary.common import Common
from HelloBikeLibrary.con_mysql import UseMysql
from HelloBikeLibrary.get_thirdInfo import ThirdInfo
from HelloBikeLibrary.base import Base

__version__ = VERSION

class HelloBikeLibrary(Request,Common,UseMysql,ThirdInfo):
	"""
		HelloBikeLibrary 1.0
	"""
	ROBOT_LIBRARY_SCOPE = "GLOBAL"

if __name__ == '__main__':
	pass