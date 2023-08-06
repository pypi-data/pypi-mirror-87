class JsConstants():
    get_element_xpath_with_index_script = """ 
                    window.shield34GetXPathWithIndexOfElement= function(element) { \n
                        if (element===document.body)\n 
                            return '//' + element.tagName;\n                        
                        var ix= 0;\n
                        var siblings= element.parentNode.childNodes;\n
                        for (var i= 0; i<siblings.length; i++) {\n
                            var sibling= siblings[i];\n
                            if (sibling===element)\n
                                return window.shield34GetXPathWithIndexOfElement(element.parentNode)+'/'+element.tagName+'['+(ix+1)+']';\n
                            if (sibling.nodeType===1 && sibling.tagName===element.tagName)\n
                                ix++;\n
                        }\n
                    };
                    return window.shield34GetXPathWithIndexOfElement(arguments[0]);
    """

    get_element_xpath_with_id_script = """
                window.shield34GetXPathWithIdOfElement = function(element, level) {\n
                    if (element.id!=='' && level !==0)\n
                        return 'id(\"'+element.id+'\")';\n
                    if (element===document.body)\n
                        return '//' + element.tagName;\n
                    var ix= 0;\n
                    var siblings= element.parentNode.childNodes;\n
                    for (var i= 0; i<siblings.length; i++) {\n
                        var sibling= siblings[i];\n
                        if (sibling===element)\n
                            return window.shield34GetXPathWithIdOfElement(element.parentNode, level+1)+'/'+element.tagName+'['+(ix+1)+']';\n
                        if (sibling.nodeType===1 && sibling.tagName===element.tagName)\n
                            ix++;\n
                    }\n
                };
                return window.shield34GetXPathWithIdOfElement(arguments[0], 0);
    """
