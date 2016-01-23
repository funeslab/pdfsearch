function Program(programid, query, pageNumber){
    this._idPage = function (programid, pageIndex){
        return programid + "-" + (pageIndex + 1).toString();
    };

    var self = this;
    this._programid = programid;
    this._pages = [];
    this._pageIndex = 0;
    for (var i=0; i < pageNumber; i++) {
        this._pages.push([this._idPage(programid, i), false]);
    }
    this._query = query;
    this._iframe = $("#" + this._programid);
    this._pageText = $("#pg_" + programid);
    this._buttonPrevMark = $("#btn_prev_" + programid);
    this._buttonNextMark = $("#btn_next_" + programid);
    this._buttonPrevPage = $("#btn_prev_pg_" + programid);
    this._buttonNextPage = $("#btn_next_pg_" + programid);
    this._buttonPDF = $("#btn_pdf_" + programid);
    this._markIndex = 0;
    this._doc = null;
    this._marks = [];
    this._isBackardNavegation = false;
    this._totalHitPage = 0;

    this.addPage = function (page, pageid) {
        for (var i=0; i < this._pages.length; i++) {
            if (this._pages[i][0] == pageid){
                this._pages[i][1] = true;
                this._totalHitPage += 1;
                break;
            }
        }
    };

    this._loadPageInIframe = function (){
        var idPage = this._idPage(this._programid, this._pageIndex);
        if (this._pages[this._pageIndex][1]) {
            var pageNumber = 0;
            for (var i=0; i <= this._pageIndex; i++)
                if (this._pages[i][1])
                    pageNumber += 1;
            $("#txt_current_" + this._programid).text(pageNumber.toString());
            q = this._query;
        } else {
            $("#txt_current_" + this._programid).text("-");
            q = "";
        }
        this._iframe.attr('src', '/page/' + idPage + q);
        this._pageText.text(this._pageIndex + 1);
    };

    this.enableDisableButtons = function () {
        // disable/enable buttons
        if (! this.prevPageMarkIndex().found
            && this._markIndex <= 0) {
            this._buttonPrevMark.prop('disabled', true);
        } else {
            this._buttonPrevMark.prop('disabled', false);
        }
        if (this._markIndex >=  this._marks.length - 1
            && ! this.nextPageMarkIndex().found) {
            this._buttonNextMark.prop('disabled', true);
        } else {
            this._buttonNextMark.prop('disabled', false);
        }
        if (this._pageIndex == 0) {
            this._buttonPrevPage.prop('disabled', true);
        } else {
            this._buttonPrevPage.prop('disabled', false);
        }
        if (this._pageIndex == this._pages.length - 1) {
            this._buttonNextPage.prop('disabled', true);
        } else {
            this._buttonNextPage.prop('disabled', false);
        }
    };

    this.nextPageMarkIndex = function () {
        var found = false;
        var index = 0;
        for (var i = this._pageIndex + 1; i < this._pages.length; i++) {
            if (this._pages[i][1]){
                index = i;
                found = true;
                break;
            }
        }
        return {
            "found": found,
            "index": index
        }
    };

    this.nextPageMark = function () {
        var next = this.nextPageMarkIndex();
        if (next.found) {
            this._pageIndex = next.index;
            this._loadPageInIframe();
        } else {
            // TODO: hide or disable button
            this._message("Última página con resultados", "Estás en la última página que tiene resultados con tu búsqueda.");
        }
    };

    this.prevPageMarkIndex = function () {
        var found = false;
        var index = 0;
        for (var i = this._pageIndex - 1; i >= 0; i--) {
            if (this._pages[i][1]){
                index = i
                found = true;
                break;
            }
        }
        return {
            "found": found,
            "index": index
        };
    };

    this.prevPageMark = function () {
        var prev = this.prevPageMarkIndex();
        if (prev.found) {
            this._pageIndex = prev.index;
            this._isBackardNavegation = true;
            this._loadPageInIframe();
        } else {
            // TODO: hide or disable button
            this._message("Primera página con resultados", "Estás en la primera página que tiene resultados con tu búsqueda.");
        }
    };

    this._mark = function () {
        xxx = this;
        var mark = this._marks.slice(this._markIndex, this._markIndex + 1);
        // TODO: change this for class!
        this._marks.css("background-color", "yellow");
        mark.css("background-color", "orange");
        this._doc.scrollTop(0);
        var offset = mark.offset().top + 8 - this._iframe.height();
        if (offset > 0) {
            this._doc.scrollTop(0);
            this._doc.scrollTop(offset + 120);
        }
        else {
            this._doc.scrollTop(0);
        }
        offset = mark.offset().left - this._iframe.width();
        if (offset > 0) {
            this._doc.scrollLeft(offset + 80);
        }
        else {
            this._doc.scrollLeft(0);
        }
        this.enableDisableButtons();
    };

    this._initFrame = function () {
        // TODO: if pdftohtml
        // this._doc = this._iframe.contents();
        // TODO: if pdf2htmlEX
        this._doc = this._iframe.contents().find("#page-container");
        this._marks = this._doc.find(".match");
        var num = this._marks.length;
        if (this._isBackardNavegation) {
            if (num > 0) {
                this._markIndex = num - 1;
            }
            this._isBackardNavegation = false;
        } else {
            this._markIndex = 0;
        }
        if (num > 0){
            this._mark();
        }
        this.enableDisableButtons();
    };


    this._doButtonPrevPage = function () {
        if (this._pageIndex > 0) {
            this._pageIndex = this._pageIndex - 1;
            this._loadPageInIframe();
        } else {
            // TODO: hide or disable button
            this._message("Primera página", "Estás en la primera página.");
        }
    };

    this._doButtonNextPage = function () {
        if (this._pageIndex < this._pages.length - 1) {
            this._pageIndex = this._pageIndex +1;
            this._loadPageInIframe();
        } else {
            // TODO: hide or disable button
            this._message("Última página", "Alcanzaste la última página.");
        }
    };

    this._doButtonNextMark = function () {
        var next = this._markIndex + 1;
        if (next < this._marks.length) {
            this._markIndex = next;
            this._mark();
        } else {
            this.nextPageMark();
        }
    };

    this._doButtonPrevMark = function () {
        var prev = this._markIndex - 1;
        if (prev >= 0) {
            this._markIndex = prev;
            this._mark();
        } else {
            this.prevPageMark();
        }
    };

    this._doButtonPDF = function () {
        var idPage = this._idPage(this._programid, this._pageIndex);
        $('#complete-pdf').attr("href", "/static/appelec/pdf/" + programid + ".pdf");
        $('#page-pdf').attr("href", "/static/appelec/pdf/" + idPage + ".pdf");
        $('#page-pdf-number').text(this._pageIndex + 1);
        $('#pdfModal').modal('show');
    };

    this._message = function (label, content) {
        $('#messageModalLabel').text(label);
        $('#messageModalContent').text(content);
        $("#messageModal").modal('show');
    };
    this.init = function () {
        for (var i = 0; i < this._pages.length; i++){
            if (this._pages[i][1]) {
                this._pageIndex = i;
                break;
            }
        }
        this._loadPageInIframe();
        this._iframe.load(function (){
            self._initFrame();
        });
        this._buttonPrevMark.click(function () {
            self._doButtonPrevMark();
        });
        this._buttonNextMark.click(function () {
            self._doButtonNextMark();
        });
        this._buttonPrevPage.click(function () {
            self._doButtonPrevPage();
        });
        this._buttonNextPage.click(function () {
            self._doButtonNextPage();
        });
        this._buttonPDF.click(function () {
            self._doButtonPDF();
        });
        $("#txt_total_" + this._programid).text(this._totalHitPage);
    }
}
