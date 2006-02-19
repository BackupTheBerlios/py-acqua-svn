from distutils.core import setup 
import glob
import py2exe 
 
setup( 
    name = 'PyAcqua', 
    description = 'Programma per la gestione degli acquari.', 
    version = '0.8', 
 
    windows = [ 
                  { 
                      'script': 'acqua.py', 
                      'icon_resources': [(1, "pyacqua.ico")], 
                  } 
              ], 
 
    options = { 
                  'py2exe': { 
                      'packages':'encodings', 
                      'includes': 'cairo, pango, pangocairo, atk, gobject, pychart, pychart.axis, pychart.area, pychart.basecanvas, pychart.canvas, pychart.line_plot, pychart.pie_plot, pychart.rose_plot, pychart.tick_mark, pychart.bar_plot, pychart.chart_data, pychart.arrow, pychart.text_box, pychart.color, pychart.font, pychart.fill_style, pychart.error_bar, pychart.range_plot, pychart.chart_object, pychart.line_style, pychart.legend, pychart.pychart_util, pychart.theme, pychart.scaling, pychart.zap, pychart.coord, pychart.linear_coord, pychart.log_coord, pychart.category_coord, pychart.afm, pychart.interval_bar_plot, pysqlite2', 
                  } 
              }, 
 
    data_files=[ 
                   ("pixmaps", glob.glob("pixmaps/*")),
				   ("files", glob.glob("files/*.txt"))
               ] 
) 