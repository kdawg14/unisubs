/* Amara, universalsubtitles.org
 *
 * Copyright (C) 2015 Participatory Culture Foundation
 *
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU Affero General Public License as
 * published by the Free Software Foundation, either version 3 of the
 * License, or (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU Affero General Public License for more details.
 *
 * You should have received a copy of the GNU Affero General Public License
 * along with this program.  If not, see
 * http://www.gnu.org/licenses/agpl-3.0.html.
 */
(function() {


$(function() {
    console.log($('a.copy-text'));
    $('a.copy-text').click(function(evt) {
        var text = $(this).data('text');
        // must use a temporary form element for the selection and copy
        var textarea = $("<textarea/>", {
            style: "position: absolute; left: -9999px; top: 0"
        });
        $(document.body).append(textarea);
        textarea.val(text);

        // select the content
        var currentFocus = document.activeElement;
        textarea.focus();
        textarea.selectRange(0, text.length);

        try {
            document.execCommand("copy");
        } catch(e) {
            console.log('Error copying text');
        }
        // restore original focus
        if (currentFocus && typeof currentFocus.focus === "function") {
            currentFocus.focus();
        }
        evt.stopPropagation();
        evt.preventDefault();
        textarea.remove();
    });
});


$.fn.selectRange = function(start, end) {
    var e = this[0];
    if (!e) return;
    else if (e.setSelectionRange) { e.focus(); e.setSelectionRange(start, end); } /* WebKit */ 
    else if (e.createTextRange) { var range = e.createTextRange(); range.collapse(true); range.moveEnd('character', end); range.moveStart('character', start); range.select(); } /* IE */
    else if (e.selectionStart) { e.selectionStart = start; e.selectionEnd = end; }
};


})();

