from airium import Airium


def test_example_template(local_file):
    """ This is an airium implementation of W3 CSS "architect" template.
        Demo: https://www.w3schools.com/w3css/tryw3css_templates_architect.htm
        TryIt: https://www.w3schools.com/w3css/tryit.asp?filename=tryw3css_templates_architect&stacked=h
    """

    lorem_ipsum = """\
        Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do
        eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad
        minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip
        ex ea commodo consequat. Excepteur sint
              occaecat cupidatat non proident, sunt in culpa qui officia
        deserunt mollit anim id est laborum consectetur adipiscing elit, sed do
        eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad
        minim veniam, quis nostrud exercitation ullamco
              laboris nisi ut aliquip ex ea commodo consequat."""

    projects = [
        [
            {'name': "Summer House", 'img': "house5.jpg"},
            {'name': "Brick House", 'img': "house2.jpg"},
            {'name': "Renovated", 'img': "house3.jpg"},
            {'name': "Barn House", 'img': "house4.jpg"}],
        [
            {'name': "Summer House", 'img': "house2.jpg", 'style': "width:99%"},
            {'name': "Brick House", 'img': "house5.jpg", 'style': "width:99%"},
            {'name': "Renovated", 'img': "house4.jpg", 'style': "width:99%"},
            {'name': "Barn House", 'img': "house3.jpg", 'style': "width:99%"}]]

    stuff = [
        {"name": "John Doe", "title": "CEO &amp; Founder", "img": 'team2.jpg'},
        {"name": "Jane Doe", "title": "Architect", "img": 'team1.jpg'},
        {"name": "Mike Ross", "title": "Architect", "img": 'team3.jpg'},
        {"name": "Dan Star", "title": "Architect", "img": 'team4.jpg'}]

    a = Airium('  ')
    a('<!DOCTYPE html>')
    with a.html(lang="pl"):
        with a.head():
            a.meta(charset="utf-8")
            a.meta(name="viewport", content="width=device-width, initial-scale=1")
            a.title(_t="Airium page title")
            a.link(rel="icon", href="https://110.120.1.14/site/img/favicon.ico", type="image/png")
            a.link(rel="stylesheet", href="https://www.w3schools.com/w3css/4/w3.css")
            a.script(src="https://code.jquery.com/jquery-3.2.1.slim.min.js")

        with a.body(klass="bodyclass"):
            with a.div(klass="w3-top"):
                with a.div(klass="w3-bar w3-white w3-wide w3-padding w3-card"):
                    with a.a(href="#home", klass="w3-bar-item w3-button"):
                        a.b(_t="BR")
                        a("Architects")

                    with a.div(klass="w3-right w3-hide-small"):
                        a.a(href="#projects", klass="w3-bar-item w3-button", _t="Projects")
                        a.a(href="#about", klass="w3-bar-item w3-button", _t="About")
                        a.a(href="#contact", klass="w3-bar-item w3-button", _t="Contact")

            with a.header(klass="w3-display-container w3-content w3-wide", style="max-width:1500px;", id="home"):
                a.img(klass="w3-image", src="https://www.w3schools.com/w3images/architect.jpg", alt="Architecture",
                      width="1500", height="800")

                with a.div(klass="w3-display-middle w3-margin-top w3-center"):
                    with a.h1(klass="w3-xxlarge w3-text-white"):
                        a.span(klass="w3-padding w3-black w3-opacity-min", _t="<b>BR</b>")

            with a.div(klass="w3-content w3-padding", style="max-width:1564px"):
                a.h3(klass="w3-border-bottom w3-border-light-grey w3-padding-16", _t="Projects")

                for row in projects:
                    with a.div(klass="w3-row-padding"):
                        for project_args in row:
                            img_style = project_args.get('style', "width:100%")
                            with a.div(klass="w3-col l3 m6 w3-margin-bottom"):
                                with a.div(klass="w3-display-container"):
                                    a.div(klass="w3-display-topleft w3-black w3-padding", _t=project_args['name'])
                                    a.img(src=f"https://www.w3schools.com/w3images/{project_args['img']}",
                                          alt=f"House {project_args['name']}", style=img_style)

                with a.div(klass="w3-container w3-padding-32", id="about"):
                    with a.h3(klass="w3-border-bottom w3-border-light-grey w3-padding-16"):
                        a("About")
                    a.p(lorem_ipsum)

                with a.div(klass="w3-row-padding w3-grayscale"):
                    for p in stuff:
                        with a.div(klass="w3-col l3 m6 w3-margin-bottom"):
                            a.img(src=f"https://www.w3schools.com/w3images/{p['img']}", alt=p['name'].split()[0],
                                  style="width:100%")
                            a.h3(p['name'])
                            a.p(klass="w3-opacity", _t=p['title'])
                            a.p(_t="Phasellus eget enim eu lectus faucibus vestibulum. "
                                   "Suspendisse sodales pellentesque elementum.")
                            with a.p():
                                a.button(klass="w3-button w3-light-grey w3-block", _t="Contact")

                with a.div(klass="w3-container w3-padding-32", id="contact"):
                    a.h3(klass="w3-border-bottom w3-border-light-grey w3-padding-16", _t='Contact')
                    a.p(_t="Lets get in touch and talk about your next project.")

                with a.form(action="/action_page.php", target="_blank"):
                    a.input(klass="w3-input w3-border", type="text", placeholder="Name", required="", name="Name")
                    a.input(klass="w3-input w3-section w3-border", type="text", placeholder="Email", required="",
                            name="Email")
                    a.input(klass="w3-input w3-section w3-border", type="text", placeholder="Subject", required="",
                            name="Subject")
                    a.input(klass="w3-input w3-section w3-border", type="text", placeholder="Comment", required="",
                            name="Comment")
                    with a.button(klass="w3-button w3-black w3-section", type="submit"):
                        a.i(klass="fa fa-paper-plane")
                        a("SEND MESSAGE")

                with a.div(klass="w3-container"):
                    a.img(src="https://www.w3schools.com/w3images/map.jpg", klass="w3-image", style="width:100%")

            with a.footer(klass="w3-center w3-black w3-padding-16"):
                with a.p(_t="Powered by "):
                    with a.a(href="https://www.w3schools.com/w3css/default.asp", title="W3.CSS", target="_blank",
                             klass="w3-hover-text-green"):
                        a("w3.css")

    reference = local_file('documents', 'w3_architects_example_synth.html')
    if not 'store':
        reference.store(str(a))

    expected = reference.contents()
    assert str(a) == expected
