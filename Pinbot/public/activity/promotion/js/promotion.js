
    jQuery(document).ready(function() {
        var starttime =  parseInt($('.promotion-time').attr('start-time'))*1000+8*60*60*1000;
        $('#countdown_dashboard').countDown({
            targetDate: {
                'starttime':starttime,
                'day':      '01',
                'month':    '02',
                'year':     '2016',
                'hour':     '00',
                'min':      '00',
                'sec':      '01'
            }
        })
    });