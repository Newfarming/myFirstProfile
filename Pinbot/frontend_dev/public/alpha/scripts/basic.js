function addMark(feed_id, resume_id, mark) {
	url = "/feed/modify_feed_result?feed_id=" + feed_id + "&resume_id=" + resume_id + "&reco_index=" + mark;
	$.getJSON(url, function (json) {

		if (json.status == true) {
			// alert(url);
			if (mark >= 0) {
				$("#" + resume_id + "_like").text("已推荐");
				$("#" + resume_id + "_dislike").hide();
			} else {
				$("#" + resume_id + "_dislike").text("已屏蔽");
				$("#" + resume_id + "_like").hide();
			}
		} else {
			alert("error: " + json.data);
		}
	});
};
