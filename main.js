const puppeteer = require('puppeteer');
const fs = require('fs');
const path = require('path');

const auth = {"username": "xxxxx", "password": "xxxx"};
const course_id = 13;
const urls = {
    "login": "http://www.tensorinfinity.com/index.php?r=front/loginpage",
    "course": `http://www.tensorinfinity.com/index.php?r=space/coursecontinue&id=${course_id}`
};

const chromeOptions = {
    headless:false,
    slowMo:50,
    // 打开开发者工具, 当此值为true时, headless总为false
    //devtools: true,
};

(async() => {
    const browser = await puppeteer.launch(chromeOptions);
    const page = await browser.newPage();
    const result = [];
    const result_filename = path.resolve(__dirname, "json", course_id + ".json");

    //login
    await page.goto(urls["login"])
    //auth
    await page.type(`#lgn_mobile`, auth["username"]);
    await page.type(`#lgn_password`, auth['password']);
    await page.click(`div.login-box button.sign-btn`);

    await page.waitFor(2000);
    console.log(urls["course"]);
    //course
    await page.goto(urls["course"]);

    //course list
    await page.click(`div.media-list-div div.media-list-tab div[data-target="lesson_list"]`)
    const course_list = await page.$$eval(`#lesson_list div a`, el => [].map.call(el, cur => {return {"href": cur.href, "text": cur.innerText}}));
    
    const course_page = await browser.newPage();
    for (var cur of course_list){
        console.log(cur["text"]);
        await course_page.goto(cur["href"]);

        //media page
        const media_page = await browser.newPage();
        //media list
        const media_list = await course_page.$$eval(`#media_list div a`, el => [].map.call(el, cur => {return {"href": cur.href, "text": cur.innerText}}));
        for(var media of media_list){
            await media_page.goto(media["href"]);
            await media_page.waitForSelector(`#aiplayer .prism-big-play-btn`);
            await media_page.click(`#aiplayer .prism-big-play-btn`);
            await media_page.waitForSelector(`#aiplayer video[src]`);
            const video_url = await media_page.$eval(`#aiplayer video`, el => el.src);
            var obj = {"file_name": media["text"] + ".mp4", "video_url": video_url, "referer": media["href"]};
            console.log("\t", obj);
            result.push(obj);
            //break;
            await media_page.waitFor(1000);
            
        }
        await media_page.close();
        //break;
    }

    //wirte result to file
    fs.writeFileSync(result_filename, JSON.stringify(result));
    //close page
    await course_page.close();
    await page.close();

    await browser.close();
})();

