(function() {
    const CLICK_MARK = 'CLICK_EVENT:';
    function getXPath(element) {
        if (element.id) {
            return '//*[@id="' + element.id + '"]';
        }
        if (element === document.body) {
            return '/html/body';
        }
        let index = 0;
        const siblings = element.parentNode.childNodes;
        for (let i = 0; i < siblings.length; i++) {
            const sibling = siblings[i];
            if (sibling === element) {
                const parentXPath = getXPath(element.parentNode);
                return parentXPath + '/' + element.tagName.toLowerCase() + '[' + (index + 1) + ']';
            }
            if (sibling.nodeType === 1 && sibling.tagName === element.tagName) {
                index++;
            }
        }
        return '';
    }
    document.addEventListener('click', function(event) {
        const target = event.target;
        if (!target || target.nodeType !== 1) return;
        const clickInfo = {
            tag: target.tagName.toLowerCase(),
            id: target.id || '',
            classes: String(target.className || ''),
            title: (target.title || 'unknown').toLowerCase(),
            text: (target.textContent || '').trim().slice(0, 50),
            xpath: getXPath(target),
            timestamp: new Date().toISOString()
        };
        console.log(CLICK_MARK, JSON.stringify(clickInfo));
    }, true);
    console.log('Click logger started!');
})();
