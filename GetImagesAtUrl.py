# coding: utf-8

import qrcode
import appex
import ui
import clipboard
import requests
from PIL import Image
from bs4 import BeautifulSoup

class MyTableViewDelegate (object):
    def __init__(self, imgUrls, view):
        self.imgUrls = imgUrls
        self.view = view
    def tableview_did_select(self, tableview, section, row):
        # Called when a row was selected.
        clipboard.set(self.imgUrls[row])
        self.view.close()
        pass

    def tableview_did_deselect(self, tableview, section, row):
        # Called when a row was de-selected (in multiple selection mode).
        pass

    def tableview_title_for_delete_button(self, tableview, section, row):
        # Return the title for the 'swipe-to-***' button.
        return 'Delete'
        
class MyTableViewDataSource (object):
    def __init__(self, imgUrls):
        self.imgUrls = imgUrls
        # create a placeholder image
        with ui.ImageContext(100,100) as ctx:
            oval = ui.Path.oval(0,0,100,100)
            ui.set_color('red')
            oval.fill()
            self.placeholder_img = ctx.get_image()
    def tableview_number_of_sections(self, tableview):
        # Return the number of sections (defaults to 1)
        return 1

    def tableview_number_of_rows(self, tableview, section):
        # Return the number of rows in the section
        return len(self.imgUrls)

    def tableview_cell_for_row(self, tableview, section, row):
        # Create and return a cell for the given section/row
        cell = ui.TableViewCell()
        cell.image_view.image = self.placeholder_img
        cell.image_view.load_from_url(self.imgUrls[row])
        cell.text_label.text = self.imgUrls[row]
        return cell

    def tableview_title_for_header(self, tableview, section):
        # Return a title for the given section.
        # If this is not implemented, no section headers will be shown.
        return 'Some Section'

    def tableview_can_delete(self, tableview, section, row):
        # Return True if the user should be able to delete the given row.
        return True

    def tableview_can_move(self, tableview, section, row):
        # Return True if a reordering control should be shown for the given row (in editing mode).
        return True

    def tableview_delete(self, tableview, section, row):
        # Called when the user confirms deletion of the given row.
        pass

    def tableview_move_row(self, tableview, from_section, from_row, to_section, to_row):
        # Called when the user moves a row with the reordering control (in editing mode).
        pass
        
def main():
	if not appex.is_running_extension():
		print('This script is intended to be run from the sharing extension.')
		print('falling back to a test url')
		url = 'http://twitter.com'
	else:
	  url = appex.get_url()
	if not url:
		print('No input URL found.')
		return
	#print(url)
	
	#do http request
	req = requests.request('GET', url);
	if req.status_code != 200:
	  print('result not 200. no good')
	  return
	
	soup = BeautifulSoup(req.text, 'html5lib')
	# get all img src attributes
	imgUrls = list(map((lambda img: img.get('src')), soup.find_all('img')))
	# filter to just .jpg .png .gif
	imgUrls = [i for i in imgUrls if i != None and i.endswith(('.jpg', '.png', '.gif'))]
	# remove duplicates
	imgUrls = list(set(imgUrls))
	
	v = ui.load_view('GetImagesAtUrl')
	tv = v['tableview']
	tv.delegate = MyTableViewDelegate(imgUrls, v)
	tv.data_source = MyTableViewDataSource(imgUrls)
	v.present()
	
if __name__ == '__main__':
	main()
