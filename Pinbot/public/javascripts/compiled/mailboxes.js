function MailboxesModel() {
    var self = this;

    self.mailboxName = ko.observable();
    self.mailboxType = ko.observable();

    self.mailboxes = ko.observableArray([]);

    self.addMailbox = function() {
        self.mailboxes.push({ name: this.mailboxName(), type: this.mailboxType() });
        self.mailboxName("");
        self.mailboxType("");
    };
}

ko.applyBindings(new MailboxesModel());
