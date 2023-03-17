from dataclasses import dataclass
@dataclass(frozen=True)
class Local:
    def __init__(self):
        self.TAG_SELECTOR = """
                {
                    // Returns the first element matching given selector in the root's subtree.
                    query(root, selector) {
                        return root.querySelector(selector);
                },
                    // Returns all elements matching given selector in the root's subtree.
                    queryAll(root, selector) {
                        return Array.from(root.querySelectorAll(selector));
                    }
                }"""
        self.MAIN_URL = 'https://lms.ssu.ac.kr/'
        self.ID_LOCATOR = "ID"
        self.PW_LOCATOR = "PW"
        self.GET_CLASS_TODO_CLASS_1_FRAME = 'div#root'
        self.FOR_ID_ITME = '#userid'
        self.FOR_PW_ITME = '#pwd'
        self.MY_PAGE= 'https://class.ssu.ac.kr/mypage'
        self.PER_URL = 'https://canvas.ssu.ac.kr'
        self.PDF_PAGE_SELECTOR ='xpath=/html/body/div[2]/div[2]/div[2]/div[3]/div[1]/div/div[1]/iframe'
        self.PDF_1_XPATH ='xpath=/html/body/div[2]/div[2]/div[2]/div[3]/div[1]/div/div[1]/iframe'
        self.PDF_2_XPATH = 'xpath=/html/body/div/div/div[2]/div[2]/iframe'
        self.PDF_3_XPATH = 'xpath=/html/body/div/div/div[2]/div[2]/iframe'
        self.PDF_URL_LOCATOR = 'meta[property="og:image"]'
        self.PDF_TITLE_LOCATOR = 'meta[property="og:title"]'
        self.CLASS_TITLE = "meta[name='title']"
        self.FILE_PAGE_SELECTOR =  'xpath=/html/body/div[2]/div[2]/div[2]/div[3]/div[1]/div/div[1]/iframe'
        self.FILE_1_XPATH = 'xpath=/html/body/div/div/div[2]/div[2]'
        self.FILE_LOCATOR = "xpath=/html/body/div/div/div[2]/div[2]"
        self.FILE_NAME_LOCATOR = '.xnbc-file-name'
        self.FILE_DOWNLOAD_LOCATOR = '.xnbc-file-download-icon'
        self.EXPAND_LOCATOR = 'iframe#tool_content'
        self.EXPAND_TEXT = '모두'
        self.EXPAND_FALSE = '모두 펼치기'
        self.PER_CLASS_URL_EXTERNAL_TOOLS = '/external_tools/71'
        self.PER_CLASS_URL_EXTERNAL_TOOLS73 = '/external_tools/73'
        self.PER_CLASS_ALL_PAGE = "#tool_content"
        self.PER_CLASS_ALL_PAGE_LOCATOR = '.xnmb-module_item-wrapper'
        self.PER_CLASS_TITLE_LOCATOR = '.xnmb-module_item-left-title.link'
        self.PER_CLASS_STATUS_LOCATOR = '.xnmb-module_item-icon'
        self.PER_CLASS_URL_LOCATOR = '.xnmb-module_item-left-title.link'
        self.PER_CLASS_DATE_CHECK ='.xnmb-module_item-meta_data-left-wrapper'
        self.PER_CLASS_DATE_LOCATOR = '.xnmb-module_item-meta_data-lecture_periods-due_at'
        self.PER_CLASS_DATE_START_LOCATOR='.xnmb-module_item-meta_data-lecture_periods-unlock_at'
        self.PER_CLASS_IS_DONE = 'xpath=/html/body/div/div/div[2]/div[4]/span[3]/span'