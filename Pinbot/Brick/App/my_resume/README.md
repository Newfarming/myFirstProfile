<div id="table-of-contents">
<h2>Table of Contents</h2>
<div id="text-table-of-contents">
<ul>
<li><a href="#sec-1">1. 简历数据库设计</a></li>
</ul>
</div>
</div>

# 简历数据库设计

<table border="2" cellspacing="0" cellpadding="6" rules="groups" frame="hsides">


<colgroup>
<col  class="left" />

<col  class="left" />

<col  class="left" />

<col  class="left" />
</colgroup>
<tbody>
<tr>
<td class="left">名称</td>
<td class="left">字段</td>
<td class="left">类型</td>
<td class="left">取值</td>
</tr>


<tr>
<td class="left">名字</td>
<td class="left">name</td>
<td class="left">varchar 30</td>
<td class="left">runforever</td>
</tr>


<tr>
<td class="left">目前薪水</td>
<td class="left">current_salary</td>
<td class="left">int</td>
<td class="left">0</td>
</tr>


<tr>
<td class="left">职位类型</td>
<td class="left">job_category</td>
<td class="left">varchar 20</td>
<td class="left">&#xa0;</td>
</tr>


<tr>
<td class="left">求职状态</td>
<td class="left">job_hunting_state</td>
<td class="left">varchar 20</td>
<td class="left">&#xa0;</td>
</tr>


<tr>
<td class="left">期望工作地</td>
<td class="left">expectation_area</td>
<td class="left">varchar 20</td>
<td class="left">四川成都</td>
</tr>


<tr>
<td class="left">期望薪水</td>
<td class="left">target_salary</td>
<td class="left">float</td>
<td class="left">1000</td>
</tr>


<tr>
<td class="left">证书信息</td>
<td class="left">certificate</td>
<td class="left">varchar 200</td>
<td class="left">思科认证</td>
</tr>


<tr>
<td class="left">QQ</td>
<td class="left">qq</td>
<td class="left">varchar 20</td>
<td class="left">348453961</td>
</tr>


<tr>
<td class="left">头像地址</td>
<td class="left">avatar_url</td>
<td class="left">varchar 200</td>
<td class="left">&#xa0;</td>
</tr>


<tr>
<td class="left">电话</td>
<td class="left">phone</td>
<td class="left">varchar 20</td>
<td class="left">18042412008</td>
</tr>


<tr>
<td class="left">邮箱</td>
<td class="left">email</td>
<td class="left">varchar 60</td>
<td class="left">runforever@163.com</td>
</tr>


<tr>
<td class="left">年龄</td>
<td class="left">age</td>
<td class="left">int</td>
<td class="left">23</td>
</tr>


<tr>
<td class="left">学校</td>
<td class="left">school</td>
<td class="left">varchar 40</td>
<td class="left">吉林大学</td>
</tr>


<tr>
<td class="left">学历</td>
<td class="left">degree</td>
<td class="left">varchar 20</td>
<td class="left">本科</td>
</tr>


<tr>
<td class="left">婚姻状况</td>
<td class="left">marital_status</td>
<td class="left">varchar 20</td>
<td class="left">未婚</td>
</tr>


<tr>
<td class="left">专业</td>
<td class="left">major</td>
<td class="left">varchar 30</td>
<td class="left">软件工程</td>
</tr>


<tr>
<td class="left">现居地</td>
<td class="left">address</td>
<td class="left">varchar 80</td>
<td class="left">四川成都</td>
</tr>


<tr>
<td class="left">常住地</td>
<td class="left">residence</td>
<td class="left">varchar 80</td>
<td class="left">四川成都</td>
</tr>


<tr>
<td class="left">工作年限</td>
<td class="left">work_years</td>
<td class="left">int</td>
<td class="left">2</td>
</tr>


<tr>
<td class="left">生日</td>
<td class="left">birthday</td>
<td class="left">datetime</td>
<td class="left">1990.11.13</td>
</tr>


<tr>
<td class="left">政治面貌</td>
<td class="left">political_landscape</td>
<td class="left">varchar 20</td>
<td class="left">团员</td>
</tr>


<tr>
<td class="left">身份证号</td>
<td class="left">identity_id</td>
<td class="left">varchar 25</td>
<td class="left">450322199011134013</td>
</tr>


<tr>
<td class="left">性别</td>
<td class="left">gender</td>
<td class="left">varchar 15</td>
<td class="left">male</td>
</tr>


<tr>
<td class="left">主页</td>
<td class="left">homepage</td>
<td class="left">varchar 200</td>
<td class="left"><https:runforever.github.io></td>
</tr>


<tr>
<td class="left">其他信息</td>
<td class="left">other_info</td>
<td class="left">textfield</td>
<td class="left">&#x2026;</td>
</tr>


<tr>
<td class="left">成就</td>
<td class="left">research_perf</td>
<td class="left">varchar 200</td>
<td class="left">无</td>
</tr>


<tr>
<td class="left">爱好</td>
<td class="left">hobbies</td>
<td class="left">varchar 100</td>
<td class="left">女</td>
</tr>


<tr>
<td class="left">语言能力</td>
<td class="left">language_skills</td>
<td class="left">varchar 100</td>
<td class="left">cet-4</td>
</tr>


<tr>
<td class="left">学校奖项</td>
<td class="left">perf_at_school</td>
<td class="left">varchar 200</td>
<td class="left">无</td>
</tr>


<tr>
<td class="left">自我评价</td>
<td class="left">self_evaluation</td>
<td class="left">varchar 400</td>
<td class="left">很NB</td>
</tr>


<tr>
<td class="left">创建时间</td>
<td class="left">create_time</td>
<td class="left">datetime</td>
<td class="left">&#xa0;</td>
</tr>


<tr>
<td class="left">更新时间</td>
<td class="left">update_time</td>
<td class="left">datetime</td>
<td class="left">&#xa0;</td>
</tr>


<tr>
<td class="left">开始时间</td>
<td class="left">start_time</td>
<td class="left">datetime</td>
<td class="left">&#xa0;</td>
</tr>


<tr>
<td class="left">结束时间</td>
<td class="left">end_time</td>
<td class="left">datetime</td>
<td class="left">&#xa0;</td>
</tr>


<tr>
<td class="left">职称</td>
<td class="left">position_title</td>
<td class="left">varchar 20</td>
<td class="left">研发工程师</td>
</tr>


<tr>
<td class="left">时长</td>
<td class="left">duration</td>
<td class="left">int</td>
<td class="left">6</td>
</tr>


<tr>
<td class="left">薪水</td>
<td class="left">salary</td>
<td class="left">float</td>
<td class="left">6700</td>
</tr>


<tr>
<td class="left">公司名称</td>
<td class="left">company_name</td>
<td class="left">varchar 40</td>
<td class="left">聘宝</td>
</tr>


<tr>
<td class="left">公司类别</td>
<td class="left">company_category</td>
<td class="left">varchar 30</td>
<td class="left">互联网</td>
</tr>


<tr>
<td class="left">行业性质</td>
<td class="left">industry_category</td>
<td class="left">varchar 20</td>
<td class="left">互联网</td>
</tr>


<tr>
<td class="left">项目描述</td>
<td class="left">project_desc</td>
<td class="left">varchar 500</td>
<td class="left">&#xa0;</td>
</tr>


<tr>
<td class="left">职责</td>
<td class="left">responsible_for</td>
<td class="left">varchar 300</td>
<td class="left">负责接口开发</td>
</tr>


<tr>
<td class="left">证书</td>
<td class="left">certificate</td>
<td class="left">varchar 60</td>
<td class="left">证书</td>
</tr>


<tr>
<td class="left">课程</td>
<td class="left">course</td>
<td class="left">varchar 80</td>
<td class="left">C++程序设计</td>
</tr>


<tr>
<td class="left">培训机构</td>
<td class="left">instituation</td>
<td class="left">varchar 60</td>
<td class="left">吉林大学C++培训</td>
</tr>


<tr>
<td class="left">位置</td>
<td class="left">location</td>
<td class="left">varchar 60</td>
<td class="left">吉林长春</td>
</tr>


<tr>
<td class="left">培训描述</td>
<td class="left">train_desc</td>
<td class="left">varchar 200</td>
<td class="left">呵呵</td>
</tr>


<tr>
<td class="left">技能描述</td>
<td class="left">skill_desc</td>
<td class="left">varchar 30</td>
<td class="left">Python</td>
</tr>


<tr>
<td class="left">技能级别</td>
<td class="left">proficiency</td>
<td class="left">varchar 20</td>
<td class="left">大师你懂吗</td>
</tr>


<tr>
<td class="left">技能时间</td>
<td class="left">month</td>
<td class="left">int</td>
<td class="left">1</td>
</tr>


<tr>
<td class="left">简历ID</td>
<td class="left">source_id</td>
<td class="left">varchar 60</td>
<td class="left">fsdafjal84329048</td>
</tr>


<tr>
<td class="left">URL的ID</td>
<td class="left">url_id</td>
<td class="left">varchar 60</td>
<td class="left">&#xa0;</td>
</tr>


<tr>
<td class="left">view的ID</td>
<td class="left">view_id</td>
<td class="left">varchar 60</td>
<td class="left">&#xa0;</td>
</tr>


<tr>
<td class="left">简历语言</td>
<td class="left">resume_language</td>
<td class="left">varchar 20</td>
<td class="left">chinese</td>
</tr>


<tr>
<td class="left">搜索关键词</td>
<td class="left">search_keyword</td>
<td class="left">varchar 40</td>
<td class="left">&#xa0;</td>
</tr>


<tr>
<td class="left">简历关键词</td>
<td class="left">resume_keyword</td>
<td class="left">varchar 40</td>
<td class="left">&#xa0;</td>
</tr>


<tr>
<td class="left">所属网站</td>
<td class="left">source</td>
<td class="left">varchar 20</td>
<td class="left">zhilian</td>
</tr>


<tr>
<td class="left">修改时间</td>
<td class="left">modify_time</td>
<td class="left">datetime</td>
<td class="left">&#xa0;</td>
</tr>


<tr>
<td class="left">最低薪水</td>
<td class="left">min_salary</td>
<td class="left">float</td>
<td class="left">6</td>
</tr>


<tr>
<td class="left">最高薪水</td>
<td class="left">max_salary</td>
<td class="left">float</td>
<td class="left">9</td>
</tr>
</tbody>
</table>
