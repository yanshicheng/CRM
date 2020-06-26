
'''
分页
'''

class Pagination():
    def __init__(self,current_page,total_count,urls='/index/',per_page=10,show_page=9):
        # 定义路径
        self.urls = urls

        # 计算显示所有数据需要多少页,如果有余数则进行加一操作
        total_page, more = divmod(total_count,per_page)
        if more:
            total_page += 1
        # 定义最大页码数
        self.total_page = total_page



        # 定义当前的页码数
        try:
            current_page = int(current_page)
        except Exception as e:
            current_page = 1
        # 页码数必须大于0
        if current_page < 1:
            current_page = 1

        # 不能大于 总页码数,否则显示最后一页
        current_page = total_page if current_page > total_page else current_page
        self.current_page = current_page
        # 定义总共数据条目是多少
        self.total_count = total_count

        # 定义每页显示的数据条目是多少
        self.per_page = per_page

        # 页面上最多显示的页码数
        self.show_page = show_page
        # 最多显示页码的一半
        self.half_show_page = show_page // 2

    @property
    def start(self):
            # 数据切片的开始位置
        return self.per_page * (self.current_page -1)

    @property
    def end(self):
        return self.current_page * self.per_page

    def page_html(self):
        # 如果总页面的页码数小于要显示的页码数
        if self.total_page <  self.show_page:
            show_page_start = 1
            show_page_end =  self.total_page
        # 判断 左边边界
        elif  self.current_page -  self.half_show_page < 1:
            show_page_start = 1
            show_page_end =  self.show_page
        elif  self.current_page +  self.half_show_page >  self.total_page:
            show_page_start =  self.total_page -  self.show_page + 1
            show_page_end =  self.total_page
        else:
            # 页面显示页码的开始
            show_page_start =  self.current_page -  self.half_show_page
            show_page_end =  self.current_page +  self.half_show_page
        # 页面显示页码的结束

        # 生成 html 代码
        page_list = []
        page_list.append('<nav aria-label="Page navigation"><ul class="pagination">')
        # 首页
        page_list.append(f'<li><a href="{self.urls}?page=1">首页</a></li>')
        page_list.append(f'<li><a href="{self.urls}?page={self.current_page - 1}" aria-label="Previous"><span aria-hidden="true">&laquo;</span></a>')

        for i in range(show_page_start, show_page_end + 1):
            if i ==  self.current_page:
                s = f' <li class="active"><a href="{self.urls}?page={i}">{i}</a></li>'
            else:
                s = f' <li><a href="{self.urls}?page={i}">{i}</a></li>'
            page_list.append(s)

        page_list.append(
            f'<li><a href="{self.urls}?page={self.current_page + 1}" aria-label="Next"><span aria-hidden="true">&raquo;</span></a>')
        # 尾页
        page_list.append(f'<li><a href="{self.urls}?page={self.total_page}">尾页</a></li>')
        page_list.append('</ul></nav>')
        page_html = ''.join(page_list)
        return page_html