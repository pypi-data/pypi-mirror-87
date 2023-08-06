 # @ Author: FAN Jianing
 # @ Create Time: 2020-12-04 15:47:59
 # @ Modified by: FAN Jianing
 # @ Modified time: 2020-12-07 17:40:36
 # @ Description: 去除掉无用glyphs以达到为字体瘦身的目的

import os
import fontTools.subset as fts
import fontTools.ttLib as ttlib 
import logging


class FontReducer(object):
    def __init__(self):
        pass

    def __load_font(self, font_path: str) -> ttlib.TTFont:
        """读取字体文件
        Args:
            font_path (str): 字体文件的路径
        Raises:
            FileExistsError: 字体文件不存在
        Returns:
            ttlib.TTFont: 返回一个字体对象
        """
        if not os.path.exists(font_path):
            raise FileExistsError("file [{}] does not exsits.".format(font_path))
        options = fts.Options()
        return fts.load_font(font_path, options)


    def __get_font_all_glyphs(self, font_path: str) -> list:
        """获取字体中所有的glyphs
        Args:
            font_path (str): 字体文件路径
        Returns:
            list: 包含所有glyphs name 的列表
        """
        font_obj = self.__load_font(font_path)
        glyphs = font_obj.getGlyphNames()
        logging.info("Load font successfully, total [{}] glyphs.".format(len(glyphs)))
        return glyphs

    def reducer_font_by_glyphs(self, font_path: str, glyphs: list)-> ttlib.TTFont:
        """根据提供的glyphs保留字体中的字
        Args:
            font_path (str): 字体的路径
            glyphs (list): 包含glyphs name的列表
        Returns:
            ttlib.TTFont: 返回一个字体对象
        """
        font_obj = self.__load_font(font_path)
        options = fts.Options()
        options.ignore_missing_glyphs = True
        options.desubroutinize = True
        subsetter = fts.Subsetter(options = options)
        subsetter.populate(glyphs = set(glyphs))
        subsetter.subset(font_obj)
        return  font_obj



    def font_match_reducer(self, source_fontpath: str, target_fontpath: str) -> ttlib.TTFont:
        """通过来源字体删除目标字体的reducer
        Args:
            source_fontpath (str): 来源字体路径
            target_fontpath (str): 目标字体路径
        Raises:
            Exception: 来源字体的glyphs为空
        Returns:
            ttlib.TTFont: 返回一个字体对象
        """
        src_glyphs = self.__get_font_all_glyphs(source_fontpath)

        if len(src_glyphs) <= 0:
            raise Exception ("glyphs of source font is empty.")

        reducer_font_obj = self.reducer_font_by_glyphs(target_fontpath, src_glyphs)
        return reducer_font_obj
       


    def write_ttf(self, output_filepath:str, font_obj:ttlib.TTFont):
        """写入字体到ttf
        Args:
            output_filepath (str): 保存字体文件的路径
            font_obj (ttlib.TTFont): 输入的字体对象
        """
        font_obj.save(output_filepath)
        logging.info("Writting font file [{}] successfully.".format(output_filepath))


if __name__ == "__main__":
  

    fr = FontReducer()
    font_path = "./btxbt.ttf"
    target_path = "./czsxsj.ttf"
    font = fr.font_match_reducer(font_path, target_path)
    fr.write_ttf("res.ttf", font)



