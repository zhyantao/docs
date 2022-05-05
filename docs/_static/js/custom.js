// Change default behavior -> Open in new tab
$(document).ready(
    function () {
        $('a.external').attr('target', '_blank');
    }
);

// Add sphinx comment module
var script = document.createElement("script");
script.type = "text/javascript";
script.src = "https://utteranc.es/client.js";
script.async = "async";

script.setAttribute("repo", "zhyantao/zhyantao.github.io");
script.setAttribute("issue-term", "pathname");
script.setAttribute("theme", "github-light");
script.setAttribute("label", "comments");
script.setAttribute("crossorigin", "anonymous");

// sections = document.querySelectorAll("div.section");
sections = document.querySelectorAll("div>section");
if (sections !== null) {
    section = sections[sections.length-1];
    section.appendChild(script);
}
