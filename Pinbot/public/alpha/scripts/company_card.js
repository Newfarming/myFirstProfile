$.CompanyInfo=function(t){return new $.CompanyInfo.prototype.init(t)},$.CompanyInfo.prototype={constructor:$.CompanyInfo,init:function(t){this.setting=$.extend({style:window.infos&&window.infos.company&&window.infos.company.key_points?"info":"edit"},t),window.$_companyInfo=this,this.appendContent(this.getHtml())},getHtml:function(t){t=t||window.$_companyInfo.setting.style;var e="",a=window.infos&&window.infos.company?window.infos.company:!1,n=a&&a.company_name?a.company_name:"",i=a&&a.key_points?a.key_points:"",s=a&&a.desc?a.desc:"",o=a&&a.company_stage?a.company_stage:"",l=a&&a.product_url?a.product_url:"",d=infos&&infos.all_company_category?infos.all_company_category:[],r=function(t,e){for(var a="",n=0,i=t.length;i>n;n++){var s=t[n],o=s.id,l=s.category,d=s.select;e?a+='<a data-id="'+o+'" class="area'+(d?" select":"")+'">'+l+"</a>":d&&(a+='<a data-id="'+o+'" class="area">'+l+"</a>")}return a};return"edit"==t?(e+='<div class="company-card-insert"><form action="" accept-charset="utf-8"><div class="insert-notice">完善企业名片，并在下载简历时选择将企业名片发送给候选人，那么此次简历下载，我们将仅扣除您3个聘宝点数，若候选人通过邮件反馈对您发布的职位感兴趣，我们再扣除您余下9个聘宝点数，若求职者对您发布的职位不感兴趣，将不再扣除您的聘宝点数！</div><table class="table company-table" width="100%" cellpadding="0" cellspacing="0"><tr><th><span class="required">企业名称</span></th><td><input type="text" name="company_name" value="'+n+'" class="input w526" data-equired data-reg="isNull"></td></tr><tr><th><span class="required">企业亮点</span></th><td><textarea class="textarea w540" placeholder="请尽量精简文字，并适当使用换行，便于候选人阅读哦（140字以内）" name="key_points" maxLength="140" data-lenlimit="140" rows="5" data-equired data-reg="isNull">'+i+'</textarea></td></tr><tr><th><span class="required">企业简介</span></th><td><textarea class="textarea w540" placeholder="请尽量精简文字，并适当使用换行，便于候选人阅读哦（300字以内）" name="desc" maxLength="300" data-lenlimit="300" rows="5">'+s+'</textarea></td></tr><tr><th><span class="required">企业发展阶段</span></th><td><input type="text" name="company_stage" value="'+o+'" class="input w526" data-equired data-reg="isNull"></td></tr><tr><th>网址</th><td><input type="text" name="product_url" value="'+l+'" class="input w526"></td></tr><tr><th><span class="required">所在领域</span><br><span class="orange">(可选3个)</span></th><td><div class="area-panel clearfix" id="JS_choose_area">'+r(d,!0)+'</div></td></tr></table><div class="company-submition text-center">',e+=window.infos.show_mission?'<a href="javascript:;" title="保存" class="btn btn-large btn-primary" id="JS_save_company">保存并新建定制</a>':'<a href="javascript:;" title="保存" class="btn btn-large btn-primary" id="JS_save_company">保 存</a>',n&&(e+='<a href="javascript:;" title="取消" class="a-blue ml10" id="JS_cancel_edit">取消</a>'),window.infos.show_mission&&(e+='<p style="color: #666666; line-height:25px; padding-top:10px;"><span class="red simsun">*</span>完成第一个专属定制提交，领取<span style="color:#ff6600;">红包</span><i class="i-envelope"></i></p>'),e+="</div></form></div>"):(s=s?s:"暂无",l=l?l:"",e+='<div class="company-card-show"><h3 class="card-title">'+n+'</h3><ul class="card-details"><li class="clearfix"><strong>企业亮点</strong><p>'+i+'</p></li><li class="clearfix"><strong>企业简介</strong><p>'+s+'</p></li><li class="clearfix"><strong>发展阶段</strong><p>'+o+'</p></li><li class="clearfix"><strong>网址</strong>',e+=l?'<p><a href="'+l+'" title="" target="_blank" class="a-blue">'+l+"</a></p>":"<p>暂无</p>",e+='</li><li class="clearfix" style="background-position:31px 13px;"><strong style="margin-top: 4px;">所在领域</strong><div class="clearfix view">'+r(d)+'</div></li></ul><p class="text-right"><a href="javascript:;" title="修改" class="button-default" id="JS_edit_company_info">修改</a></p></div>'),e},saveCompanyAjax:function(t){var e="/companycard/company/save/",a=this,n=function(){for(var e=t.category,a=window.infos.all_company_category,n=[],i=0,s=a.length;s>i;i++){var o=a[i];o.select=!1;for(var l=0,d=e.length;d>l;l++){var r=e[l];r==o.id&&(o.select=!0)}n.push(o)}window.infos.all_company_category=n};$.post(e,JSON.stringify(t),function(e){if(e&&"ok"==e.status){if(window.infos&&window.infos.show_mission&&e.redirect_url)return void(location.href=e.redirect_url);window.infos&&window.infos.company&&window.infos.company.key_points||a.showAddJob(),n(),window.infos.company=t,window.$_companyInfo.saveAfter()}else e&&e.msg?$.alert('<p style="text-align:center; font-size:14px; color:#333;padding:30px 0;"><i class="i-l-notice"></i>'+e.msg+"</p>"):$.alert('<p style="text-align:center; font-size:14px; color:#333;padding:30px 0;"><i class="i-l-notice"></i>请求失败，请刷新后再试！</p>')},"json")},showAddJob:function(){var t=function(){$._intentionCard?($._intentionCard.addJob(),$("#JS_add_job").click()):setTimeout(t,100)};t()},saveAfter:function(){window.$_companyInfo.appendContent(window.$_companyInfo.getHtml("info"))},appendContent:function(t){$("#JS_company_info").html(t)}},$.CompanyInfo.prototype.init.prototype=$.CompanyInfo.prototype,$.intentionCard=function(t){return new $.intentionCard.prototype.init(t)},$.intentionCard.prototype={constructor:$.intentionCard,init:function(t){this.setting=$.extend({list:[],allowSend:!1,synOnly:!1,contentDom:"#JS_jobs_list",callback:null},t),$._intentionCard=this,this.appendList(this.getList()),window.infos&&window.infos.company&&window.infos.company.key_points&&!this.setting.allowSend&&(!window.infos.jobs||$.isEmptyObject(infos.jobs))&&this.addJob(),"function"==typeof this.setting.callback&&this.setting.callback()},templates:function(t,e){var a="",n=window.infos&&window.infos.company&&window.infos.company.company_name?window.infos.company.company_name:"",i="",s="",o="",l="",d="",r="",c={0:"不限",1:"一年以上",3:"三年以上",5:"五年以上"},p="",f="",u="",m={0:"不限",3:"专科",4:"本科",7:"硕士",10:"博士"};switch(e&&(s=e.id,i=e.title,o=+e.salary_low/1e3,l=+e.salary_high/1e3,d=e.address,r=e.work_years,p=e.degree,f=e.desc,u=e.skill_desc),t){case"new":a+='<div class="job-panel"><div class="border"></div><div class="job-info"><a href="javascript:;" title="新增岗位" class="add-job-btn" id="JS_add_job">新增岗位</a></div></div>';break;case"edit":f="暂无"==f?"":f,u="暂无"==u?"":u,a+='<div class="job-panel"><div class="border"></div><div class="job-info"><h3 class="card-title arr">'+n+'</h3><div class="job-details"><form action="" method="get" accept-charset="utf-8"><table class="table company-table job-table" width="100%" cellpadding="0" cellspacing="0"><tr><th><span class="red simsun">*</span>职位名称</th><td><input type="text" name="title" value="'+i+'" class="input w220" data-equired data-reg="isNull"></td></tr><tr><th><span class="red simsun">*</span>薪资范围</th><td><input type="text" name="salary_low" value="'+o+'" class="input w70 inline" data-equired data-reg="price"> K&nbsp;&nbsp;-&nbsp;&nbsp;<input type="text" name="salary_high" value="'+l+'" class="input w70 inline" data-equired data-reg="price"> K</td></tr><tr><th><span class="red simsun">*</span>工作地点</th><td><input type="text" name="address" value="'+d+'" class="input w220" data-equired data-reg="isNull"></td></tr><tr><th><span class="red simsun">*</span>最低工作年限</th><td><div class="drop-select left w246" style="*z-index:190"><button class="button" type="button" data-toggle="dropdown">'+(r?c[r]:"不限")+'<i class="i-barr"></i></button><div class="drop-box"><ul class="drop-down"><li><a '+("0"==r?'class="active"':"")+">不限</a></li><li><a "+("1"==r?'class="active"':"")+">一年以上</a></li><li><a "+("3"==r?'class="active"':"")+">三年以上</a></li><li><a "+("5"==r?'class="active"':"")+'>五年以上</a></li></ul></div><select name="work_years" class="JS_proficiency"><option value="0" '+("0"==r?"selected":"")+'>不限</option><option value="1" '+("1"==r?"selected":"")+'>一年以上</option><option value="3" '+("3"==r?"selected":"")+'>三年以上</option><option value="5" '+("5"==r?"selected":"")+'>五年以上</option></select></div></td></tr><tr><th><span class="red simsun">*</span>最低学历</th><td><div class="drop-select left w246" style="*z-index:190"><button class="button" type="button" data-toggle="dropdown">'+(p?m[p]:"不限")+'<i class="i-barr"></i></button><div class="drop-box"><ul class="drop-down"><li><a '+("0"==p?'class="active"':"")+">不限</a></li><li><a "+("3"==p?'class="active"':"")+">专科</a></li><li><a "+("4"==p?'class="active"':"")+">本科</a></li><li><a "+("7"==p?'class="active"':"")+">硕士</a></li><li><a "+("10"==p?'class="active"':"")+'>博士</a></li></ul></div><select name="degree" class="JS_proficiency"><option value="0" '+("0"==p?"selected":"")+'>不限</option><option value="3" '+("3"==p?"selected":"")+'>专科</option><option value="4" '+("4"==p?"selected":"")+'>本科</option><option value="7" '+("7"==p?"selected":"")+'>硕士</option><option value="10" '+("10"==p?"selected":"")+'>博士</option></select></div></td></tr><tr><th>职位描述</th><td><textarea class="textarea w275" name="desc">'+f+'</textarea></td></tr><tr><th>岗位要求</th><td><textarea class="textarea w275" name="skill_desc">'+u+'</textarea></td></tr></table><p class="job-handles" data-id="'+s+'"><a href="javascript:;" title="保存" class="button-active JS_save_job">保存</a> <a href="javascript:;" title="取消" class="button-default JS_cancel_save">取消</a></p></form></div></div></div>';break;case"info":f=""==f?"暂无":f,u=""==u?"暂无":u,a+='<div class="job-panel"><div class="border"></div><div class="job-info"><h3 class="card-title arr">'+n,this.setting.allowSend||this.setting.synOnly||(a+='<a href="javascript:;" class="i-del JS_delete_job" data-id="'+s+'"></a>'),a+='</h3><div class="job-details"><table class="table company-table job-table" width="100%" cellpadding="0" cellspacing="0"><tr><th><span class="red simsun">*</span>职位名称</th><td><span>'+i+'</span></td></tr><tr><th><span class="red simsun">*</span>薪资范围</th><td><span>'+o+"K - "+l+'K</span></td></tr><tr><th><span class="red simsun">*</span>工作地点</th><td><span>'+d+'</span></td></tr><tr><th><span class="red simsun">*</span>最低工作年限</th><td><span>'+c[r]+'</span></td></tr><tr><th><span class="red simsun">*</span>最低学历</th><td><span>'+m[p]+"</span></td></tr><tr><th>职位描述</th><td><span>"+f+"</span></td></tr><tr><th>岗位要求</th><td><span>"+u+'</span></td></tr></table><p class="job-handles mt31" data-id="'+s+'">',this.setting.allowSend&&(a+='<a href="javascript:;" title="发送" class="button-default JS_send_job_to_user">发送</a> '),a+=this.setting.synOnly?'<a href="javascript:;" title="同步" class="button-default JS_syn_job_btn">同步</a> ':'<a href="javascript:;" title="修改" class="button-default JS_edit_job_btn">修改</a> <a href="/companycard/job/preview/'+s+'/" title="预览" class="button-default" target="_blank">预览</a>',a+="</p></div></div></div>"}return a},getList:function(){var t=this.setting,e=t.list,a=(t.page,""),n={};if(!e.length)return window.infos.jobs=n,a;for(var i=0,s=e.length;s>i;i++){var o=e[i],l=o.id;a+=this.templates("info",o),n[l]=o}return window.infos.jobs=n,this.setting.allowSend||this.setting.synOnly||(a+=this.templates("new")),a},saveSuccess:function(t,e){var a=t.closest(".job-panel");a.before(this.templates("info",e)).remove(),$("#JS_add_job").length||this.setting.allowSend||$(this.setting.contentDom).append($._intentionCard.templates("new"))},jobShowEdit:function(t,e){var a=t.closest(".job-panel"),n="";n=$._intentionCard.templates("edit",window.infos.jobs[e]),a.after(n).remove()},cancelEdit:function(t,e){var a=t.closest(".job-panel"),n="";n=e?$._intentionCard.templates("info",window.infos.jobs[e]):$._intentionCard.templates("new"),a.after(n).remove()},addJob:function(){$._intentionCard.appendList($._intentionCard.templates("new"))},insertJob:function(){$._intentionCard.appendList($._intentionCard.templates("edit"))},deleteJob:function(t,e){if(e){var a="/companycard/job/delete/"+e+"/",n=function(){$.get(a,{},function(a){a&&"ok"==a.status?(t.closest(".job-panel").remove(),delete window.infos.jobs[e],$.isEmptyObject(infos.jobs)&&!$("#JS_add_job").length&&$._intentionCard.addJob()):a&&a.msg?$.alert('<p style="text-align:center; font-size:14px; color:#333;padding:30px 0;"><i class="i-l-notice"></i>'+a.msg+"</p>"):$.alert('<p style="text-align:center; font-size:14px; color:#333;padding:30px 0;"><i class="i-l-notice"></i>请求失败，请刷新后再试！</p>')})};1==$(".JS_delete_job").length?$.confirm('<p style="text-align:center; font-size:14px; color:#333;padding:30px 0;"><i class="i-l-notice"></i>您只有一条岗位信息了，删除后无法生成企业名片，确认要删除吗？</p>',n):n()}},appendList:function(t){$(this.setting.contentDom).html(t)}},$.intentionCard.prototype.init.prototype=$.intentionCard.prototype;var cardScroll=function(t){t=$.extend({boxDom:"#JS_jobs_ajax_content",tagClass:"job-panel",leftBtn:"#JS_left_btn",rightBtn:"#JS_right_btn",stepCount:2,present:0,step:870},t);var e=function(){t.present<=0&&(t.present=0,$(t.leftBtn).hide()),t.present>=t.len&&(t.present=t.len,$(t.rightBtn).hide()),t.present>0&&$(t.leftBtn).show(),t.present<t.len&&$(t.rightBtn).show(),$(t.boxDom).animate({left:-t.step*t.present+"px"},"slow")},a=null,n=$(t.boxDom).find("."+t.tagClass).length;n&&(a=Math.ceil(n/2),$(t.boxDom).css("width",t.step*a+"px"),t.len=a-1,0==t.len&&$(t.rightBtn).hide(),$(t.leftBtn).hide(),$(t.rightBtn).on("click",function(){t.present++,e()}),$(t.leftBtn).on("click",function(){t.present--,e()}))},chooseSynCard=function(){var t=$("#JS_syn_cards").html(),e=jobList||[],a=925;1==e.length&&(a=490),$.LayerOut({html:t,closeByShadow:!1,dialogCss:"width:"+a+"px; height:610px;"}),$.intentionCard({list:e,synOnly:!0,allowSend:!1,contentDom:"#JS_jobs_ajax_content",callback:cardScroll})};$(function(){$(document).on("click","#JS_save_company",function(){var t=$(this),e=t.closest("form"),a=e.serializeObject(),n=!0,i=$("#JS_choose_area .select");if(a.company_name||(e.find('input[name="company_name"]').addClass("tip-error"),n=!1),a.key_points&&a.key_points!=e.find('textarea[name="key_points"]').attr("placeholder")||(e.find('textarea[name="key_points"]').addClass("tip-error"),n=!1),a.company_stage||(e.find('input[name="company_stage"]').addClass("tip-error"),n=!1),e.find("[maxLength]").each(function(){var t=$(this),e=t.attr("maxLength"),a=t.val(),i="请控制在"+e+"字以内，精简的文字更便于候选人阅读哦！",s=t.attr("name");return a.length>e?("key_points"==s?i="企业亮点"+i:"desc"==s&&(i="企业简介"+i),t.addClass("tip-error"),n=!1,$.alert(i),!1):void 0}),i.length){for(var s=[],o=0,l=i.length;l>o;o++){var d=i.eq(o);id=d.attr("data-id"),s.push(id)}a.category=s}else $.alert('<p style="text-align:center; font-size:14px; color:#333;padding:30px 0;"><i class="i-l-notice"></i>请选择所在领域！</p>'),n=!1;return n?(a.desc==e.find('textarea[name="desc"]').attr("placeholder")&&(a.desc=""),void window.$_companyInfo.saveCompanyAjax(a)):!1}),$(document).on("click","#JS_cancel_edit",function(){window.$_companyInfo.appendContent(window.$_companyInfo.getHtml("info"))}),$(document).on("click","#JS_edit_company_info",function(){window.$_companyInfo.appendContent(window.$_companyInfo.getHtml("edit"))}),$(document).on("click","#JS_add_job",function(){$(".JS_cancel_save").click(),$(this).closest(".job-panel").before($._intentionCard.templates("edit")).remove()}),$(document).on("click",".JS_save_job",function(){if(window.sockJob)return!1;window.sockJob=!0;var t=$(this),e=t.parent().attr("data-id"),a=t.closest("form"),n=a.serializeObject(),i=!0;return n.title||(a.find('input[name="title"]').addClass("tip-error"),i=!1),n.salary_low&&regs.price.test(n.salary_low)||(a.find('input[name="salary_low"]').addClass("tip-error"),i=!1),n.salary_high&&regs.price.test(n.salary_high)||(a.find('input[name="salary_high"]').addClass("tip-error"),i=!1),+n.salary_high<=+n.salary_low&&(a.find('input[name="salary_low"]').addClass("tip-error"),a.find('input[name="salary_high"]').addClass("tip-error"),i=!1),n.work_years||(a.find('select[name="work_years"]').addClass("tip-error"),i=!1),n.address||(a.find('input[name="address"]').addClass("tip-error"),i=!1),n.degree||(a.find('select[name="degree"]').siblings("button").addClass("tip-error"),i=!1),i?(e&&(n.id=e),n.salary_high=1e3*+n.salary_high,n.salary_low=1e3*+n.salary_low,void $.post("/companycard/job/save/",JSON.stringify(n),function(e){e&&"ok"==e.status?(n.id||(n.id=e.id),window.infos.jobs[e.id]=n,window.$._intentionCard.saveSuccess(t,n)):e&&e.msg?$.alert('<p style="text-align:center; font-size:14px; color:#333;padding:30px 0;"><i class="i-l-notice"></i>'+e.msg+"</p>"):$.alert('<p style="text-align:center; font-size:14px; color:#333;padding:30px 0;"><i class="i-l-notice"></i>请求失败，请刷新后再试！</p>'),window.sockJob=!1},"json").fail(function(){window.sockJob=!1})):(window.sockJob=!1,!1)}),$(document).on("click",".JS_cancel_save",function(){var t=$(this),e=t.parent().attr("data-id");window.$._intentionCard.cancelEdit(t,e)}),$(document).on("click",".JS_edit_job_btn",function(){var t=$(this),e=t.parent().attr("data-id");$(".JS_cancel_save").click(),window.$._intentionCard.jobShowEdit(t,e)}),$(document).on("click",".JS_delete_job",function(){var t=$(this),e=t.attr("data-id");window.$._intentionCard.deleteJob(t,e)}),$(document).on("click",".JS_send_job_to_user",function(){var t="/companycard/card/send/",e=$("#main").attr("data-resumeid"),a=$(this),n=$("#main").attr("data-feed_id"),i=a.parent().attr("data-id");return i&&e?a.attr("disabled")?!1:(a.attr("disabled",!0),void $.post(t,{feed_id:n,resume_id:e,job_id:i},function(t){if(a.attr("disabled",!1),t&&"ok"==t.status){var n=function(t,e){var a=new Date;a.setTime(a.getTime()+864e3),document.cookie=t+"="+e+";expires="+a.toUTCString()+";path=/;"};n("isSendCompanyCard"+e,1),$.alert('<p style="text-align:center; font-size:14px; color:#333;padding:30px 0;"><i class="i-l-notice"></i>企业名片发送成功！稍后请在“简历中心”中查看候选人的反馈信息。</p>',function(){location.reload()})}else t&&t.msg?$.alert('<p style="text-align:center; font-size:14px; color:#333;padding:30px 0;"><i class="i-l-notice"></i>'+t.msg+"</p>"):$.alert('<p style="text-align:center; font-size:14px; color:#333;padding:30px 0;"><i class="i-l-notice"></i>请求失败，请刷新后再试！</p>')},"json")):($.alert("缺少数据"),!1)}),$(document).on("click","#JS_syn_btn",chooseSynCard),$(document).on("click",".JS_syn_job_btn",function(){var t=$(this).closest(".job-panel"),e=t.find("tr").eq(5).find("span").html(),a=t.find("tr").eq(6).find("span").html(),n=e+"\r\n\r\n"+a;$('textarea[name="job_desc"]').val(n),$._LayerOut.close()}),$(document).on("click","#JS_choose_area a",function(){var t=$(this),e=t.hasClass("select");return $("#JS_choose_area a.select").length>=3&&!e?!1:void t.toggleClass("select")})});