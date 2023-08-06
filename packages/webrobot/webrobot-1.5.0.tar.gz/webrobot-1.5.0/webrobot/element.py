class Element:
    element = None

    def __init__(self, element):
        self.element = element

    def click(self):
        try:
            self.element.click()
            return True
        except Exception as e:
            print(e, e.__traceback__.tb_lineno)
            return False

    # 点击

    def write(self, text):
        try:
            self.element.send_keys(text)
            return True
        except Exception as e:
            print(e, e.__traceback__.tb_lineno)
            return False

    # 写入

    def clear(self):
        try:
            self.element.clear()
            return True
        except Exception as e:
            print(e, e.__traceback__.tb_lineno)
            return False

    # 清空文本内容

    def submit(self):
        try:
            self.element.submit()
            return True
        except Exception as e:
            print(e, e.__traceback__.tb_lineno)
            return False

    # 提交表单

    def clear(self):
        try:
            self.element.clear()
            return True
        except Exception as e:
            print(e, e.__traceback__.tb_lineno)
            return False

    def clear(self):
        try:
            self.element.clear()
            return True
        except Exception as e:
            print(e, e.__traceback__.tb_lineno)
            return False

    def clear(self):
        try:
            self.element.clear()
            return True
        except Exception as e:
            print(e, e.__traceback__.tb_lineno)
            return False

    def clear(self):
        try:
            self.element.clear()
            return True
        except Exception as e:
            print(e, e.__traceback__.tb_lineno)
            return False

    def clear(self):
        try:
            self.element.clear()
            return True
        except Exception as e:
            print(e, e.__traceback__.tb_lineno)
            return False

    def clear(self):
        try:
            self.element.clear()
            return True
        except Exception as e:
            print(e, e.__traceback__.tb_lineno)
            return False

    def clear(self):
        try:
            self.element.clear()
            return True
        except Exception as e:
            print(e, e.__traceback__.tb_lineno)
            return False

    def clear(self):
        try:
            self.element.clear()
            return True
        except Exception as e:
            print(e, e.__traceback__.tb_lineno)
            return False

    def clear(self):
        try:
            self.element.clear()
            return True
        except Exception as e:
            print(e, e.__traceback__.tb_lineno)
            return False

    def clear(self):
        try:
            self.element.clear()
            return True
        except Exception as e:
            print(e, e.__traceback__.tb_lineno)
            return False

    def get_attr(self, attr_name: str):
        try:
            return self.element.get_attribute(attr_name)
        except Exception as e:
            print(e, e.__traceback__.tb_lineno)
            return None

    # 获取属性值

    def get_css(self, property_name):
        try:
            return self.element.value_of_css_property(property_name)
        except Exception as e:
            print(e, e.__traceback__.tb_lineno)
            return None

    # 获取CSS值

    @property
    def text(self):
        try:
            return self.element.text
        except Exception as e:
            print(e, e.__traceback__.tb_lineno)
            return None

    @property
    def selected(self):
        try:
            return self.element.is_selected()
        except Exception as e:
            print(e, e.__traceback__.tb_lineno)
            return None

    @property
    def enabled(self):
        try:
            return self.element.is_enabled()
        except Exception as e:
            print(e, e.__traceback__.tb_lineno)
            return None

    @property
    def displayed(self):
        try:
            return self.element.is_displayed()
        except Exception as e:
            print(e, e.__traceback__.tb_lineno)
            return None

    @property
    def x(self):
        try:
            return int(self.element.location['x'])
        except Exception as e:
            print(e, e.__traceback__.tb_lineno)
            return None

    @property
    def y(self):
        try:
            return int(self.element.location['y'])
        except Exception as e:
            print(e, e.__traceback__.tb_lineno)
            return None

    @property
    def src(self):
        try:
            return self.element.get_attribute("src")
        except Exception as e:
            print(e, e.__traceback__.tb_lineno)
            return None

    @property
    def class_name(self):
        try:
            return self.element.get_attribute("class")
        except Exception as e:
            print(e, e.__traceback__.tb_lineno)
            return None

    @property
    def node_type(self):
        try:
            return self.element.get_attribute("node-type")
        except Exception as e:
            print(e, e.__traceback__.tb_lineno)
            return None

    @property
    def action_data(self):
        try:
            return self.element.get_attribute("action-data")
        except Exception as e:
            print(e, e.__traceback__.tb_lineno)
            return None

    @property
    def action_type(self):
        try:
            return self.element.get_attribute("action-type")
        except Exception as e:
            print(e, e.__traceback__.tb_lineno)
            return None

    @property
    def href(self):
        try:
            return self.element.get_attribute("href")
        except Exception as e:
            print(e, e.__traceback__.tb_lineno)
            return None

    @property
    def action_history(self):
        try:
            return self.element.get_attribute("action-history")
        except Exception as e:
            print(e, e.__traceback__.tb_lineno)
            return None

    @property
    def value(self):
        try:
            return self.element.get_attribute("value")
        except Exception as e:
            print(e, e.__traceback__.tb_lineno)
            return None

    @property
    def suda_uatrack(self):
        try:
            return self.element.get_attribute("suda-uatrack")
        except Exception as e:
            print(e, e.__traceback__.tb_lineno)
            return None

    @property
    def behavior(self):
        try:
            return self.element.get_attribute("behavior")
        except Exception as e:
            print(e, e.__traceback__.tb_lineno)
            return None

    @property
    def direction(self):
        try:
            return self.element.get_attribute("direction")
        except Exception as e:
            print(e, e.__traceback__.tb_lineno)
            return None

    @property
    def loop(self):
        try:
            return self.element.get_attribute("loop")
        except Exception as e:
            print(e, e.__traceback__.tb_lineno)
            return None

    @property
    def width(self):
        try:
            return self.element.get_attribute("width")
        except Exception as e:
            print(e, e.__traceback__.tb_lineno)
            return None

    @property
    def height(self):
        try:
            return self.element.get_attribute("height")
        except Exception as e:
            print(e, e.__traceback__.tb_lineno)
            return None

    @property
    def bgcolor(self):
        try:
            return self.element.get_attribute("bgcolor")
        except Exception as e:
            print(e, e.__traceback__.tb_lineno)
            return None

    @property
    def scrollamount(self):
        try:
            return self.element.get_attribute("scrollamount")
        except Exception as e:
            print(e, e.__traceback__.tb_lineno)
            return None

    @property
    def scrolldelay(self):
        try:
            return self.element.get_attribute("scrolldelay")
        except Exception as e:
            print(e, e.__traceback__.tb_lineno)
            return None

    @property
    def onmouseover(self):
        try:
            return self.element.get_attribute("onmouseover")
        except Exception as e:
            print(e, e.__traceback__.tb_lineno)
            return None

    @property
    def color(self):
        try:
            return self.element.get_attribute("color")
        except Exception as e:
            print(e, e.__traceback__.tb_lineno)
            return None

    @property
    def alt(self):
        try:
            return self.element.get_attribute("alt")
        except Exception as e:
            print(e, e.__traceback__.tb_lineno)
            return None

    @property
    def border(self):
        try:
            return self.element.get_attribute("border")
        except Exception as e:
            print(e, e.__traceback__.tb_lineno)
            return None

    @property
    def aling(self):
        try:
            return self.element.get_attribute("aling")
        except Exception as e:
            print(e, e.__traceback__.tb_lineno)
            return None

    @property
    def background(self):
        try:
            return self.element.get_attribute("background")
        except Exception as e:
            print(e, e.__traceback__.tb_lineno)
            return None

    @property
    def borderclor(self):
        try:
            return self.element.get_attribute("borderclor")
        except Exception as e:
            print(e, e.__traceback__.tb_lineno)
            return None

    @property
    def borderclordark(self):
        try:
            return self.element.get_attribute("borderclordark")
        except Exception as e:
            print(e, e.__traceback__.tb_lineno)
            return None

    @property
    def borderclorlight(self):
        try:
            return self.element.get_attribute("borderclorlight")
        except Exception as e:
            print(e, e.__traceback__.tb_lineno)
            return None

    @property
    def cellpadding(self):
        try:
            return self.element.get_attribute("cellpadding")
        except Exception as e:
            print(e, e.__traceback__.tb_lineno)
            return None

    @property
    def cellspacing(self):
        try:
            return self.element.get_attribute("cellspacing")
        except Exception as e:
            print(e, e.__traceback__.tb_lineno)
            return None

    @property
    def cols(self):
        try:
            return self.element.get_attribute("cols")
        except Exception as e:
            print(e, e.__traceback__.tb_lineno)
            return None

    @property
    def frame(self):
        try:
            return self.element.get_attribute("frame")
        except Exception as e:
            print(e, e.__traceback__.tb_lineno)
            return None

    @property
    def colspan(self):
        try:
            return self.element.get_attribute("colspan")
        except Exception as e:
            print(e, e.__traceback__.tb_lineno)
            return None

    @property
    def rowspan(self):
        try:
            return self.element.get_attribute("rowspan")
        except Exception as e:
            print(e, e.__traceback__.tb_lineno)
            return None

    @property
    def rows(self):
        try:
            return self.element.get_attribute("rows")
        except Exception as e:
            print(e, e.__traceback__.tb_lineno)
            return None

    @property
    def name(self):
        try:
            return self.element.get_attribute("name")
        except Exception as e:
            print(e, e.__traceback__.tb_lineno)
            return None

    @property
    def noresize(self):
        try:
            return self.element.get_attribute("noresize")
        except Exception as e:
            print(e, e.__traceback__.tb_lineno)
            return None

    # ERROR?!

    @property
    def action(self):
        try:
            return self.element.get_attribute("action")
        except Exception as e:
            print(e, e.__traceback__.tb_lineno)
            return None

    @property
    def method(self):
        try:
            return self.element.get_attribute("method")
        except Exception as e:
            print(e, e.__traceback__.tb_lineno)
            return None

    @property
    def type(self):
        try:
            return self.element.get_attribute("type")
        except Exception as e:
            print(e, e.__traceback__.tb_lineno)
            return None

    @property
    def accesskey(self):
        try:
            return self.element.get_attribute("accesskey")
        except Exception as e:
            print(e, e.__traceback__.tb_lineno)
            return None

    @property
    def contenteditable(self):
        try:
            return self.element.get_attribute("contenteditable")
        except Exception as e:
            print(e, e.__traceback__.tb_lineno)
            return None

    @property
    def contextmenu(self):
        try:
            return self.element.get_attribute("contextmenu")
        except Exception as e:
            print(e, e.__traceback__.tb_lineno)
            return None

    @property
    def dir(self):
        try:
            return self.element.get_attribute("dir")
        except Exception as e:
            print(e, e.__traceback__.tb_lineno)
            return None

    @property
    def draggable(self):
        try:
            return self.element.get_attribute("draggable")
        except Exception as e:
            print(e, e.__traceback__.tb_lineno)
            return None

    @property
    def dropzone(self):
        try:
            return self.element.get_attribute("dropzone")
        except Exception as e:
            print(e, e.__traceback__.tb_lineno)
            return None

    @property
    def hidden(self):
        try:
            return self.element.get_attribute("hidden")
        except Exception as e:
            print(e, e.__traceback__.tb_lineno)
            return None

    @property
    def id(self):
        try:
            return self.element.get_attribute("id")
        except Exception as e:
            print(e, e.__traceback__.tb_lineno)
            return None

    @property
    def lang(self):
        try:
            return self.element.get_attribute("lang")
        except Exception as e:
            print(e, e.__traceback__.tb_lineno)
            return None

    @property
    def spellcheck(self):
        try:
            return self.element.get_attribute("spellcheck")
        except Exception as e:
            print(e, e.__traceback__.tb_lineno)
            return None

    @property
    def style(self):
        try:
            return self.element.get_attribute("style")
        except Exception as e:
            print(e, e.__traceback__.tb_lineno)
            return None

    @property
    def tabindex(self):
        try:
            return self.element.get_attribute("tabindex")
        except Exception as e:
            print(e, e.__traceback__.tb_lineno)
            return None

    @property
    def title(self):
        try:
            return self.element.get_attribute("title")
        except Exception as e:
            print(e, e.__traceback__.tb_lineno)
            return None

    @property
    def translate(self):
        try:
            return self.element.get_attribute("translate")
        except Exception as e:
            print(e, e.__traceback__.tb_lineno)
            return None

    @property
    def charset(self):
        try:
            return self.element.get_attribute("charset")
        except Exception as e:
            print(e, e.__traceback__.tb_lineno)
            return None

    @property
    def coords(self):
        try:
            return self.element.get_attribute("coords")
        except Exception as e:
            print(e, e.__traceback__.tb_lineno)
            return None

    @property
    def download(self):
        try:
            return self.element.get_attribute("download")
        except Exception as e:
            print(e, e.__traceback__.tb_lineno)
            return None

    @property
    def hreflang(self):
        try:
            return self.element.get_attribute("hreflang")
        except Exception as e:
            print(e, e.__traceback__.tb_lineno)
            return None

    @property
    def media(self):
        try:
            return self.element.get_attribute("media")
        except Exception as e:
            print(e, e.__traceback__.tb_lineno)
            return None

    @property
    def rel(self):
        try:
            return self.element.get_attribute("rel")
        except Exception as e:
            print(e, e.__traceback__.tb_lineno)
            return None

    @property
    def rev(self):
        try:
            return self.element.get_attribute("rev")
        except Exception as e:
            print(e, e.__traceback__.tb_lineno)
            return None

    @property
    def shape(self):
        try:
            return self.element.get_attribute("shape")
        except Exception as e:
            print(e, e.__traceback__.tb_lineno)
            return None

    @property
    def target(self):
        try:
            return self.element.get_attribute("target")
        except Exception as e:
            print(e, e.__traceback__.tb_lineno)
            return None

    @property
    def onclick(self):
        try:
            return self.element.get_attribute("onclick")
        except Exception as e:
            print(e, e.__traceback__.tb_lineno)
            return None

    @property
    def ondblclick(self):
        try:
            return self.element.get_attribute("ondblclick")
        except Exception as e:
            print(e, e.__traceback__.tb_lineno)
            return None

    @property
    def onmousedown(self):
        try:
            return self.element.get_attribute("onmousedown")
        except Exception as e:
            print(e, e.__traceback__.tb_lineno)
            return None

    @property
    def onmouseup(self):
        try:
            return self.element.get_attribute("onmouseup")
        except Exception as e:
            print(e, e.__traceback__.tb_lineno)
            return None

    @property
    def onmousemove(self):
        try:
            return self.element.get_attribute("onmousemove")
        except Exception as e:
            print(e, e.__traceback__.tb_lineno)
            return None

    @property
    def onmouseout(self):
        try:
            return self.element.get_attribute("onmouseout")
        except Exception as e:
            print(e, e.__traceback__.tb_lineno)
            return None

    @property
    def onkeypress(self):
        try:
            return self.element.get_attribute("onkeypress")
        except Exception as e:
            print(e, e.__traceback__.tb_lineno)
            return None

    @property
    def onkeydown(self):
        try:
            return self.element.get_attribute("onkeydown")
        except Exception as e:
            print(e, e.__traceback__.tb_lineno)
            return None

    @property
    def onkeyup(self):
        try:
            return self.element.get_attribute("onkeyup")
        except Exception as e:
            print(e, e.__traceback__.tb_lineno)
            return None

    @property
    def code(self):
        try:
            return self.element.get_attribute("code")
        except Exception as e:
            print(e, e.__traceback__.tb_lineno)
            return None

    @property
    def object(self):
        try:
            return self.element.get_attribute("object")
        except Exception as e:
            print(e, e.__traceback__.tb_lineno)
            return None

    @property
    def align(self):
        try:
            return self.element.get_attribute("align")
        except Exception as e:
            print(e, e.__traceback__.tb_lineno)
            return None

    # ERROR?!

    @property
    def archive(self):
        try:
            return self.element.get_attribute("archive")
        except Exception as e:
            print(e, e.__traceback__.tb_lineno)
            return None

    @property
    def codebase(self):
        try:
            return self.element.get_attribute("codebase")
        except Exception as e:
            print(e, e.__traceback__.tb_lineno)
            return None

    @property
    def hspace(self):
        try:
            return self.element.get_attribute("hspace")
        except Exception as e:
            print(e, e.__traceback__.tb_lineno)
            return None

    @property
    def vspace(self):
        try:
            return self.element.get_attribute("vspace")
        except Exception as e:
            print(e, e.__traceback__.tb_lineno)
            return None

    @property
    def nohref(self):
        try:
            return self.element.get_attribute("nohref")
        except Exception as e:
            print(e, e.__traceback__.tb_lineno)
            return None

    @property
    def autoplay(self):
        try:
            return self.element.get_attribute("autoplay")
        except Exception as e:
            print(e, e.__traceback__.tb_lineno)
            return None

    @property
    def controls(self):
        try:
            return self.element.get_attribute("controls")
        except Exception as e:
            print(e, e.__traceback__.tb_lineno)
            return None

    @property
    def muted(self):
        try:
            return self.element.get_attribute("muted")
        except Exception as e:
            print(e, e.__traceback__.tb_lineno)
            return None

    @property
    def preload(self):
        try:
            return self.element.get_attribute("preload")
        except Exception as e:
            print(e, e.__traceback__.tb_lineno)
            return None

    @property
    def face(self):
        try:
            return self.element.get_attribute("face")
        except Exception as e:
            print(e, e.__traceback__.tb_lineno)
            return None

    @property
    def size(self):
        try:
            return self.element.get_attribute("size")
        except Exception as e:
            print(e, e.__traceback__.tb_lineno)
            return None

    @property
    def cite(self):
        try:
            return self.element.get_attribute("cite")
        except Exception as e:
            print(e, e.__traceback__.tb_lineno)
            return None

    @property
    def alink(self):
        try:
            return self.element.get_attribute("alink")
        except Exception as e:
            print(e, e.__traceback__.tb_lineno)
            return None

    @property
    def link(self):
        try:
            return self.element.get_attribute("link")
        except Exception as e:
            print(e, e.__traceback__.tb_lineno)
            return None

    @property
    def vlink(self):
        try:
            return self.element.get_attribute("vlink")
        except Exception as e:
            print(e, e.__traceback__.tb_lineno)
            return None

    @property
    def autofocus(self):
        try:
            return self.element.get_attribute("autofocus")
        except Exception as e:
            print(e, e.__traceback__.tb_lineno)
            return None

    @property
    def disabled(self):
        try:
            return self.element.get_attribute("disabled")
        except Exception as e:
            print(e, e.__traceback__.tb_lineno)
            return None

    @property
    def form(self):
        try:
            return self.element.get_attribute("form")
        except Exception as e:
            print(e, e.__traceback__.tb_lineno)
            return None

    @property
    def formaction(self):
        try:
            return self.element.get_attribute("formaction")
        except Exception as e:
            print(e, e.__traceback__.tb_lineno)
            return None

    @property
    def formenctype(self):
        try:
            return self.element.get_attribute("formenctype")
        except Exception as e:
            print(e, e.__traceback__.tb_lineno)
            return None

    @property
    def formmethod(self):
        try:
            return self.element.get_attribute("formmethod")
        except Exception as e:
            print(e, e.__traceback__.tb_lineno)
            return None

    @property
    def formnovalidate(self):
        try:
            return self.element.get_attribute("formnovalidate")
        except Exception as e:
            print(e, e.__traceback__.tb_lineno)
            return None

    @property
    def formtarget(self):
        try:
            return self.element.get_attribute("formtarget")
        except Exception as e:
            print(e, e.__traceback__.tb_lineno)
            return None

    @property
    def valign(self):
        try:
            return self.element.get_attribute("valign")
        except Exception as e:
            print(e, e.__traceback__.tb_lineno)
            return None

    @property
    def char(self):
        try:
            return self.element.get_attribute("char")
        except Exception as e:
            print(e, e.__traceback__.tb_lineno)
            return None

    @property
    def charoff(self):
        try:
            return self.element.get_attribute("charoff")
        except Exception as e:
            print(e, e.__traceback__.tb_lineno)
            return None

    @property
    def span(self):
        try:
            return self.element.get_attribute("span")
        except Exception as e:
            print(e, e.__traceback__.tb_lineno)
            return None

    @property
    def checked(self):
        try:
            return self.element.get_attribute("checked")
        except Exception as e:
            print(e, e.__traceback__.tb_lineno)
            return None

    @property
    def icon(self):
        try:
            return self.element.get_attribute("icon")
        except Exception as e:
            print(e, e.__traceback__.tb_lineno)
            return None

    @property
    def label(self):
        try:
            return self.element.get_attribute("label")
        except Exception as e:
            print(e, e.__traceback__.tb_lineno)
            return None

    @property
    def radiogroup(self):
        try:
            return self.element.get_attribute("radiogroup")
        except Exception as e:
            print(e, e.__traceback__.tb_lineno)
            return None

    @property
    def datetime(self):
        try:
            return self.element.get_attribute("datetime")
        except Exception as e:
            print(e, e.__traceback__.tb_lineno)
            return None

    @property
    def open(self):
        try:
            return self.element.get_attribute("open")
        except Exception as e:
            print(e, e.__traceback__.tb_lineno)
            return None

    @property
    def compact(self):
        try:
            return self.element.get_attribute("compact")
        except Exception as e:
            print(e, e.__traceback__.tb_lineno)
            return None

    @property
    def accept(self):
        try:
            return self.element.get_attribute("accept")
        except Exception as e:
            print(e, e.__traceback__.tb_lineno)
            return None

    @property
    def accept_charset(self):
        try:
            return self.element.get_attribute("accept-charset")
        except Exception as e:
            print(e, e.__traceback__.tb_lineno)
            return None

    @property
    def autocomplete(self):
        try:
            return self.element.get_attribute("autocomplete")
        except Exception as e:
            print(e, e.__traceback__.tb_lineno)
            return None

    @property
    def enctype(self):
        try:
            return self.element.get_attribute("enctype")
        except Exception as e:
            print(e, e.__traceback__.tb_lineno)
            return None

    @property
    def novalidate(self):
        try:
            return self.element.get_attribute("novalidate")
        except Exception as e:
            print(e, e.__traceback__.tb_lineno)
            return None

    @property
    def frameborder(self):
        try:
            return self.element.get_attribute("frameborder")
        except Exception as e:
            print(e, e.__traceback__.tb_lineno)
            return None

    @property
    def longdesc(self):
        try:
            return self.element.get_attribute("longdesc")
        except Exception as e:
            print(e, e.__traceback__.tb_lineno)
            return None

    @property
    def marginheight(self):
        try:
            return self.element.get_attribute("marginheight")
        except Exception as e:
            print(e, e.__traceback__.tb_lineno)
            return None

    @property
    def marginwidth(self):
        try:
            return self.element.get_attribute("marginwidth")
        except Exception as e:
            print(e, e.__traceback__.tb_lineno)
            return None

    @property
    def scrolling(self):
        try:
            return self.element.get_attribute("scrolling")
        except Exception as e:
            print(e, e.__traceback__.tb_lineno)
            return None

    @property
    def profile(self):
        try:
            return self.element.get_attribute("profile")
        except Exception as e:
            print(e, e.__traceback__.tb_lineno)
            return None

    @property
    def noshade(self):
        try:
            return self.element.get_attribute("noshade")
        except Exception as e:
            print(e, e.__traceback__.tb_lineno)
            return None

    @property
    def manifest(self):
        try:
            return self.element.get_attribute("manifest")
        except Exception as e:
            print(e, e.__traceback__.tb_lineno)
            return None

    @property
    def xmlns(self):
        try:
            return self.element.get_attribute("xmlns")
        except Exception as e:
            print(e, e.__traceback__.tb_lineno)
            return None

    @property
    def sandbox(self):
        try:
            return self.element.get_attribute("sandbox")
        except Exception as e:
            print(e, e.__traceback__.tb_lineno)
            return None

    @property
    def seamless(self):
        try:
            return self.element.get_attribute("seamless")
        except Exception as e:
            print(e, e.__traceback__.tb_lineno)
            return None

    @property
    def srcdoc(self):
        try:
            return self.element.get_attribute("srcdoc")
        except Exception as e:
            print(e, e.__traceback__.tb_lineno)
            return None

    @property
    def ismap(self):
        try:
            return self.element.get_attribute("ismap")
        except Exception as e:
            print(e, e.__traceback__.tb_lineno)
            return None

    @property
    def usemap(self):
        try:
            return self.element.get_attribute("usemap")
        except Exception as e:
            print(e, e.__traceback__.tb_lineno)
            return None

    @property
    def list(self):
        try:
            return self.element.get_attribute("list")
        except Exception as e:
            print(e, e.__traceback__.tb_lineno)
            return None

    @property
    def max(self):
        try:
            return self.element.get_attribute("max")
        except Exception as e:
            print(e, e.__traceback__.tb_lineno)
            return None

    @property
    def maxlength(self):
        try:
            return self.element.get_attribute("maxlength")
        except Exception as e:
            print(e, e.__traceback__.tb_lineno)
            return None

    @property
    def min(self):
        try:
            return self.element.get_attribute("min")
        except Exception as e:
            print(e, e.__traceback__.tb_lineno)
            return None

    @property
    def multiple(self):
        try:
            return self.element.get_attribute("multiple")
        except Exception as e:
            print(e, e.__traceback__.tb_lineno)
            return None

    @property
    def pattern(self):
        try:
            return self.element.get_attribute("pattern")
        except Exception as e:
            print(e, e.__traceback__.tb_lineno)
            return None

    @property
    def placeholder(self):
        try:
            return self.element.get_attribute("placeholder")
        except Exception as e:
            print(e, e.__traceback__.tb_lineno)
            return None

    @property
    def readonly(self):
        try:
            return self.element.get_attribute("readonly")
        except Exception as e:
            print(e, e.__traceback__.tb_lineno)
            return None

    @property
    def required(self):
        try:
            return self.element.get_attribute("required")
        except Exception as e:
            print(e, e.__traceback__.tb_lineno)
            return None

    @property
    def step(self):
        try:
            return self.element.get_attribute("step")
        except Exception as e:
            print(e, e.__traceback__.tb_lineno)
            return None

    @property
    def challenge(self):
        try:
            return self.element.get_attribute("challenge")
        except Exception as e:
            print(e, e.__traceback__.tb_lineno)
            return None

    @property
    def keytype(self):
        try:
            return self.element.get_attribute("keytype")
        except Exception as e:
            print(e, e.__traceback__.tb_lineno)
            return None

    @property
    def attr_for(self):
        try:
            return self.element.get_attribute("for")
        except Exception as e:
            print(e, e.__traceback__.tb_lineno)
            return None

    @property
    def default(self):
        try:
            return self.element.get_attribute("default")
        except Exception as e:
            print(e, e.__traceback__.tb_lineno)
            return None

    @property
    def content(self):
        try:
            return self.element.get_attribute("content")
        except Exception as e:
            print(e, e.__traceback__.tb_lineno)
            return None

    @property
    def http_equiv(self):
        try:
            return self.element.get_attribute("http-equiv")
        except Exception as e:
            print(e, e.__traceback__.tb_lineno)
            return None

    @property
    def scheme(self):
        try:
            return self.element.get_attribute("scheme")
        except Exception as e:
            print(e, e.__traceback__.tb_lineno)
            return None

    @property
    def low(self):
        try:
            return self.element.get_attribute("low")
        except Exception as e:
            print(e, e.__traceback__.tb_lineno)
            return None

    @property
    def high(self):
        try:
            return self.element.get_attribute("high")
        except Exception as e:
            print(e, e.__traceback__.tb_lineno)
            return None

    @property
    def optimum(self):
        try:
            return self.element.get_attribute("optimum")
        except Exception as e:
            print(e, e.__traceback__.tb_lineno)
            return None

    @property
    def classid(self):
        try:
            return self.element.get_attribute("classid")
        except Exception as e:
            print(e, e.__traceback__.tb_lineno)
            return None

    @property
    def codetype(self):
        try:
            return self.element.get_attribute("codetype")
        except Exception as e:
            print(e, e.__traceback__.tb_lineno)
            return None

    @property
    def data(self):
        try:
            return self.element.get_attribute("data")
        except Exception as e:
            print(e, e.__traceback__.tb_lineno)
            return None

    @property
    def declare(self):
        try:
            return self.element.get_attribute("declare")
        except Exception as e:
            print(e, e.__traceback__.tb_lineno)
            return None

    @property
    def standby(self):
        try:
            return self.element.get_attribute("standby")
        except Exception as e:
            print(e, e.__traceback__.tb_lineno)
            return None

    @property
    def reversed(self):
        try:
            return self.element.get_attribute("reversed")
        except Exception as e:
            print(e, e.__traceback__.tb_lineno)
            return None

    @property
    def start(self):
        try:
            return self.element.get_attribute("start")
        except Exception as e:
            print(e, e.__traceback__.tb_lineno)
            return None

    @property
    def selected(self):
        try:
            return self.element.get_attribute("selected")
        except Exception as e:
            print(e, e.__traceback__.tb_lineno)
            return None

    @property
    def valuetype(self):
        try:
            return self.element.get_attribute("valuetype")
        except Exception as e:
            print(e, e.__traceback__.tb_lineno)
            return None

    @property
    def attr_async(self):
        try:
            return self.element.get_attribute("async")
        except Exception as e:
            print(e, e.__traceback__.tb_lineno)
            return None

    @property
    def defer(self):
        try:
            return self.element.get_attribute("defer")
        except Exception as e:
            print(e, e.__traceback__.tb_lineno)
            return None

    @property
    def language(self):
        try:
            return self.element.get_attribute("language")
        except Exception as e:
            print(e, e.__traceback__.tb_lineno)
            return None

    @property
    def rules(self):
        try:
            return self.element.get_attribute("rules")
        except Exception as e:
            print(e, e.__traceback__.tb_lineno)
            return None

    @property
    def summary(self):
        try:
            return self.element.get_attribute("summary")
        except Exception as e:
            print(e, e.__traceback__.tb_lineno)
            return None

    @property
    def abbr(self):
        try:
            return self.element.get_attribute("abbr")
        except Exception as e:
            print(e, e.__traceback__.tb_lineno)
            return None

    @property
    def axis(self):
        try:
            return self.element.get_attribute("axis")
        except Exception as e:
            print(e, e.__traceback__.tb_lineno)
            return None

    @property
    def nowrap(self):
        try:
            return self.element.get_attribute("nowrap")
        except Exception as e:
            print(e, e.__traceback__.tb_lineno)
            return None

    @property
    def scope(self):
        try:
            return self.element.get_attribute("scope")
        except Exception as e:
            print(e, e.__traceback__.tb_lineno)
            return None

    @property
    def wrap(self):
        try:
            return self.element.get_attribute("wrap")
        except Exception as e:
            print(e, e.__traceback__.tb_lineno)
            return None

    @property
    def pubdate(self):
        try:
            return self.element.get_attribute("pubdate")
        except Exception as e:
            print(e, e.__traceback__.tb_lineno)
            return None

    @property
    def kind(self):
        try:
            return self.element.get_attribute("kind")
        except Exception as e:
            print(e, e.__traceback__.tb_lineno)
            return None

    @property
    def srclang(self):
        try:
            return self.element.get_attribute("srclang")
        except Exception as e:
            print(e, e.__traceback__.tb_lineno)
            return None

    @property
    def poster(self):
        try:
            return self.element.get_attribute("poster")
        except Exception as e:
            print(e, e.__traceback__.tb_lineno)
            return None
