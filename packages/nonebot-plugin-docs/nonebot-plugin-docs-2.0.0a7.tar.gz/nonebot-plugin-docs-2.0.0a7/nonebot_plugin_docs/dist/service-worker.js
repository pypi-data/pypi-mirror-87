/**
 * Welcome to your Workbox-powered service worker!
 *
 * You'll need to register this file in your web app and you should
 * disable HTTP caching for this file too.
 * See https://goo.gl/nhQhGp
 *
 * The rest of the code is auto-generated. Please don't update this file
 * directly; instead, make changes to your Workbox build configuration
 * and re-run your build process.
 * See https://goo.gl/2aRDsh
 */

importScripts("https://storage.googleapis.com/workbox-cdn/releases/4.3.1/workbox-sw.js");

self.addEventListener('message', (event) => {
  if (event.data && event.data.type === 'SKIP_WAITING') {
    self.skipWaiting();
  }
});

/**
 * The workboxSW.precacheAndRoute() method efficiently caches and responds to
 * requests for URLs in the manifest.
 * See https://goo.gl/S9QRab
 */
self.__precacheManifest = [
  {
    "url": "2.0.0a6/advanced/index.html",
    "revision": "dbd68374dd97069a5d42f98c2380a4fd"
  },
  {
    "url": "2.0.0a6/advanced/permission.html",
    "revision": "174e5cdac43baa91b175cdc16221dbc6"
  },
  {
    "url": "2.0.0a6/advanced/runtime-hook.html",
    "revision": "6376813b6e5ede246486445c48b6889f"
  },
  {
    "url": "2.0.0a6/advanced/scheduler.html",
    "revision": "9a54711957833d992d33005004bbfdc5"
  },
  {
    "url": "2.0.0a6/api/adapters/cqhttp.html",
    "revision": "bca36f8fc1e775306e90d42f8787ba04"
  },
  {
    "url": "2.0.0a6/api/adapters/index.html",
    "revision": "4dcf2fbd22dcbfaf50f22d52c3d08700"
  },
  {
    "url": "2.0.0a6/api/config.html",
    "revision": "464ccb0c24ccbaad05bcc500f3035a4e"
  },
  {
    "url": "2.0.0a6/api/drivers/fastapi.html",
    "revision": "f8975ce3b97d95fc8787fad4e618de23"
  },
  {
    "url": "2.0.0a6/api/drivers/index.html",
    "revision": "6d8932c95ca3c5fcec6960b589aae8e7"
  },
  {
    "url": "2.0.0a6/api/exception.html",
    "revision": "00e5b3b55ccb3b9e5777c5e01a2c24a7"
  },
  {
    "url": "2.0.0a6/api/index.html",
    "revision": "ccbf55b902ae9f7b2ddab1a5726d7f84"
  },
  {
    "url": "2.0.0a6/api/log.html",
    "revision": "5e8203dd6e2b0d9808d612545d611a5f"
  },
  {
    "url": "2.0.0a6/api/matcher.html",
    "revision": "a96925b67e451751f49f8d67e7beb8c3"
  },
  {
    "url": "2.0.0a6/api/message.html",
    "revision": "cf8654a0bdd943719c82dca892c43d01"
  },
  {
    "url": "2.0.0a6/api/nonebot.html",
    "revision": "b6eaacddaee01149725cb888a00f247f"
  },
  {
    "url": "2.0.0a6/api/permission.html",
    "revision": "36d0c1618466b8bf5f9c53a398b49d6e"
  },
  {
    "url": "2.0.0a6/api/plugin.html",
    "revision": "58caa0b1c035b0ddebd0122e075a3fed"
  },
  {
    "url": "2.0.0a6/api/rule.html",
    "revision": "103c4c47bca58de7eaf92e1a91e4bd3f"
  },
  {
    "url": "2.0.0a6/api/sched.html",
    "revision": "3b2d8cb596bd3390dc631d23d8ee8820"
  },
  {
    "url": "2.0.0a6/api/typing.html",
    "revision": "ddf38307486667446cdb386d8d4d8de0"
  },
  {
    "url": "2.0.0a6/api/utils.html",
    "revision": "d06a4b970fe8ede1e40de3d38dff1602"
  },
  {
    "url": "2.0.0a6/guide/basic-configuration.html",
    "revision": "6b99e4f4dd8a97d0929cf7d5379c1c2e"
  },
  {
    "url": "2.0.0a6/guide/creating-a-handler.html",
    "revision": "e74080411a4af562f0a47da6ab921543"
  },
  {
    "url": "2.0.0a6/guide/creating-a-matcher.html",
    "revision": "c19504d31907c3add2817e800d7dbcc8"
  },
  {
    "url": "2.0.0a6/guide/creating-a-plugin.html",
    "revision": "093578a9166bc4c9b00805c27ba87c57"
  },
  {
    "url": "2.0.0a6/guide/creating-a-project.html",
    "revision": "d625f46343d17afac4a8599fcb1807fb"
  },
  {
    "url": "2.0.0a6/guide/end-or-start.html",
    "revision": "7014d17fc4e1cefbf7d615f1789ebd14"
  },
  {
    "url": "2.0.0a6/guide/getting-started.html",
    "revision": "bd7cc3814137dc315646754f713e5d6b"
  },
  {
    "url": "2.0.0a6/guide/index.html",
    "revision": "70dce27d35defcaa35e238f7ec25704f"
  },
  {
    "url": "2.0.0a6/guide/installation.html",
    "revision": "6a9d40eae9f00ff3c5e87e7f1e5845ff"
  },
  {
    "url": "2.0.0a6/guide/loading-a-plugin.html",
    "revision": "1b4b4813ca8b36ed884bb4b7dbd41105"
  },
  {
    "url": "2.0.0a6/index.html",
    "revision": "d96e12034b94c95f09c58e6e9aaa53aa"
  },
  {
    "url": "404.html",
    "revision": "19c702145aa6ca3452251db6f9509ec5"
  },
  {
    "url": "advanced/export-and-require.html",
    "revision": "d15125579e73d520ca8f85c88c0f93ac"
  },
  {
    "url": "advanced/index.html",
    "revision": "9ad06e1370dde08e133b8d716a03f7b8"
  },
  {
    "url": "advanced/permission.html",
    "revision": "de3b3d64e03b5085b4314aa3d1c53be9"
  },
  {
    "url": "advanced/publish-plugin.html",
    "revision": "b54d322db37fa67e745a2d57215af21f"
  },
  {
    "url": "advanced/runtime-hook.html",
    "revision": "17162e7ce7ac8b936084a4e46a3ca1ab"
  },
  {
    "url": "advanced/scheduler.html",
    "revision": "9fedb6384e42a96aafc7be863f8dc855"
  },
  {
    "url": "api/adapters/cqhttp.html",
    "revision": "11ff86d84a15ad3b5eece8722c8e99b0"
  },
  {
    "url": "api/adapters/ding.html",
    "revision": "68cc5731db5d63d87be04f0bc4727933"
  },
  {
    "url": "api/adapters/index.html",
    "revision": "412a0b62c5e32aff8762fd97316b554e"
  },
  {
    "url": "api/config.html",
    "revision": "96b6017e80ef660221ac59ea253a4ef6"
  },
  {
    "url": "api/drivers/fastapi.html",
    "revision": "14c8409bc4d9e6ca017eeeacb6cd7bab"
  },
  {
    "url": "api/drivers/index.html",
    "revision": "9c29632c85136807d4c9c40d29ceebcb"
  },
  {
    "url": "api/exception.html",
    "revision": "be56742d95df924abeff305d4a29ebfb"
  },
  {
    "url": "api/index.html",
    "revision": "2d5d014c0bc8b0311e81c33bdf89c563"
  },
  {
    "url": "api/log.html",
    "revision": "21a7fb73c72249abab331d17a6b08ce5"
  },
  {
    "url": "api/matcher.html",
    "revision": "deabcc713a63ff46ab55a3b3d6e06435"
  },
  {
    "url": "api/message.html",
    "revision": "80ce5d66acce3cac5c86c8d9bdbeb47c"
  },
  {
    "url": "api/nonebot.html",
    "revision": "8f64c75d089e97c1ecbd3126743f2940"
  },
  {
    "url": "api/permission.html",
    "revision": "c8c98479904096acff4f08eb47645bdd"
  },
  {
    "url": "api/plugin.html",
    "revision": "972c642460536e1330e70d2f190d3bce"
  },
  {
    "url": "api/rule.html",
    "revision": "453ffc9194afde1409abb3e781a69586"
  },
  {
    "url": "api/typing.html",
    "revision": "a6a751639bfcdf6d82c0ee7f4183e044"
  },
  {
    "url": "api/utils.html",
    "revision": "663439244a4769c70b88f51144c8b096"
  },
  {
    "url": "assets/css/0.styles.7c6a3dbf.css",
    "revision": "462d2aeec3bb45377259af631cd4bb8b"
  },
  {
    "url": "assets/img/search.237d6f6a.svg",
    "revision": "237d6f6a3fe211d00a61e871a263e9fe"
  },
  {
    "url": "assets/img/search.83621669.svg",
    "revision": "83621669651b9a3d4bf64d1a670ad856"
  },
  {
    "url": "assets/js/10.916c4130.js",
    "revision": "c09a64d27e7312a40e16abc0247d6705"
  },
  {
    "url": "assets/js/100.476895b4.js",
    "revision": "d4856a6d528c8105ad92834a470ba4d6"
  },
  {
    "url": "assets/js/101.fa42cce0.js",
    "revision": "71261a934b46f0ccacb39fcbe372d5f2"
  },
  {
    "url": "assets/js/102.441f2df6.js",
    "revision": "2b937304185589327391ca7399001a91"
  },
  {
    "url": "assets/js/103.f982df3b.js",
    "revision": "3061b5c417f44b2b8890fcbcfe170b90"
  },
  {
    "url": "assets/js/104.42db27e4.js",
    "revision": "cc201109b03d527aeedf23f193efe747"
  },
  {
    "url": "assets/js/105.c4837c8d.js",
    "revision": "ec3a3f7294b9dbb8d93617878dfaa4ed"
  },
  {
    "url": "assets/js/106.0d30fa19.js",
    "revision": "5810f12a42d72daa48f1a56e7cb126a9"
  },
  {
    "url": "assets/js/107.b67c51b0.js",
    "revision": "51be801add5df67ebf682f1cf9e8e3ff"
  },
  {
    "url": "assets/js/108.31b43f55.js",
    "revision": "0f9e8550866b1b252f19ee73e8cf648e"
  },
  {
    "url": "assets/js/109.09498dbe.js",
    "revision": "cbf03e10660c4caac1f74ba682224dd5"
  },
  {
    "url": "assets/js/11.113d7571.js",
    "revision": "e2330c5ea08648ab3373943cabf25794"
  },
  {
    "url": "assets/js/110.5dbfda64.js",
    "revision": "b7ceec08597e02d0e65da2941e9e5263"
  },
  {
    "url": "assets/js/111.435e754b.js",
    "revision": "91d4487656db0c0d08c6b4f97c4a16ad"
  },
  {
    "url": "assets/js/12.f66abede.js",
    "revision": "c3f9d83989a444253d91c6e834c1f7d9"
  },
  {
    "url": "assets/js/13.72385ae5.js",
    "revision": "666eef25182e3a70c54eb4abc2236317"
  },
  {
    "url": "assets/js/14.6a92d1b2.js",
    "revision": "225869e64e4083b3d1acaa77d2ab9d2e"
  },
  {
    "url": "assets/js/15.1e7c69b4.js",
    "revision": "50625b0eb46035db643cc1b21b678c8c"
  },
  {
    "url": "assets/js/16.25a17a7e.js",
    "revision": "25cc1753117f346f758a066deccf2d06"
  },
  {
    "url": "assets/js/17.a419fd31.js",
    "revision": "8a980b93afb5f61a7fa45603455e0be4"
  },
  {
    "url": "assets/js/18.8ba34be2.js",
    "revision": "4e253c81c70cec316c7def309a10a63c"
  },
  {
    "url": "assets/js/19.2505b3df.js",
    "revision": "0f5185fdc403c09846531e5f48f86c3c"
  },
  {
    "url": "assets/js/2.c84f7eb9.js",
    "revision": "69bb4fc50d5d4831886aa38cb858ad97"
  },
  {
    "url": "assets/js/20.35e13123.js",
    "revision": "db8b4048dbc0ffc64bba933d19f221fd"
  },
  {
    "url": "assets/js/21.89bbf06d.js",
    "revision": "5c6c7e5ef1c8a3cf6851ee3021366eac"
  },
  {
    "url": "assets/js/22.4466df3b.js",
    "revision": "3228b9d805d99cc84deea17fb5596c05"
  },
  {
    "url": "assets/js/23.dec0e0e1.js",
    "revision": "ed7c4cc9cf509165d4ea12ebe45f6bc7"
  },
  {
    "url": "assets/js/24.9a25357a.js",
    "revision": "1cdb77e0db6d6de1aafc5baec4e26c41"
  },
  {
    "url": "assets/js/25.9169a191.js",
    "revision": "811d54652f55966ba2f3c2112c0e734c"
  },
  {
    "url": "assets/js/26.5c92c2ea.js",
    "revision": "39fd7441b948a0b02e80d7fa27749417"
  },
  {
    "url": "assets/js/27.52a66abd.js",
    "revision": "5f2cde18fe18cdc0b875e9073b9a4e53"
  },
  {
    "url": "assets/js/28.6a1e1137.js",
    "revision": "1c206ba037227d653cc1e40e711c5b37"
  },
  {
    "url": "assets/js/29.85be5748.js",
    "revision": "b82da35baade1087fab15b78fd724f1f"
  },
  {
    "url": "assets/js/3.6ac0001e.js",
    "revision": "a18786ebde083c89a85f04e87c0c8b84"
  },
  {
    "url": "assets/js/30.4ad30f15.js",
    "revision": "3488b33aba24da67fcd87887c74a7427"
  },
  {
    "url": "assets/js/31.061ba580.js",
    "revision": "27526cdac0cc490b10ad865d0f3aa4b8"
  },
  {
    "url": "assets/js/32.f39d2f0a.js",
    "revision": "41077c0411b6f19b214ba049a3ad232a"
  },
  {
    "url": "assets/js/33.03b84a71.js",
    "revision": "3d283b9219f065f43dd3fc55f39a2c1a"
  },
  {
    "url": "assets/js/34.c130dd25.js",
    "revision": "ddac7e96bc9ff8536071dd0fab0b11d4"
  },
  {
    "url": "assets/js/35.e9ca843e.js",
    "revision": "b5c1425de822f0412e41dd4626931216"
  },
  {
    "url": "assets/js/36.cdf26a6b.js",
    "revision": "03a036a289dc5d65a7ac2521186beef5"
  },
  {
    "url": "assets/js/37.5f1e3b8b.js",
    "revision": "b2131ac5029ca9c7571e65747cd81b9e"
  },
  {
    "url": "assets/js/38.41a4e3dd.js",
    "revision": "eae8f0d6ba1fb316b06c4730353ecf61"
  },
  {
    "url": "assets/js/39.05abe34f.js",
    "revision": "20320f29a0924c0436fb1a1764fd6259"
  },
  {
    "url": "assets/js/4.8df46d24.js",
    "revision": "71fee54f67a404aca2a106ab41e63e5e"
  },
  {
    "url": "assets/js/40.e2617959.js",
    "revision": "d564346f0dc33fc50ed8047af32b2ee8"
  },
  {
    "url": "assets/js/41.4a2951e3.js",
    "revision": "2336c6d43b860034e1cc4dcb596a4cfe"
  },
  {
    "url": "assets/js/42.a5ccd438.js",
    "revision": "ed8837dc76253f4005d0c60fd8a04f4b"
  },
  {
    "url": "assets/js/43.34f36a39.js",
    "revision": "097b4185f66f1f0c0a7e90d28595b698"
  },
  {
    "url": "assets/js/44.eed5fea4.js",
    "revision": "468366f33cab724354ff8808d1916fa9"
  },
  {
    "url": "assets/js/45.55d06824.js",
    "revision": "c8ba6dd44bea6f61efa218dfa45e63bc"
  },
  {
    "url": "assets/js/46.4b996b92.js",
    "revision": "4a431e6b1975c43a9b8cab651b5c0f88"
  },
  {
    "url": "assets/js/47.c686a9ec.js",
    "revision": "840d795f760daaab77cfa17dd64b5477"
  },
  {
    "url": "assets/js/48.3325a505.js",
    "revision": "29bb1808d8dbcbb81f20585d6b27c5dc"
  },
  {
    "url": "assets/js/49.a6715294.js",
    "revision": "55954a4951fe23f378ad71120a76d4e0"
  },
  {
    "url": "assets/js/5.1299c054.js",
    "revision": "077af6c44ce4d6790e08acadf1b55cf6"
  },
  {
    "url": "assets/js/50.57082e77.js",
    "revision": "60f1a4463b35c9e0c56a3065763bd757"
  },
  {
    "url": "assets/js/51.43025e7d.js",
    "revision": "0fc8bf96c839a1606893220232198f92"
  },
  {
    "url": "assets/js/52.fa396087.js",
    "revision": "68fadb7708dab06f8110186bdbda500f"
  },
  {
    "url": "assets/js/53.9835a80d.js",
    "revision": "077f6245cb033facf63f60c4f991a17c"
  },
  {
    "url": "assets/js/54.0c41c18b.js",
    "revision": "a573dbaf674655a9b74de171371a2806"
  },
  {
    "url": "assets/js/55.d9bbb8da.js",
    "revision": "dcbabf0d067b7b0b18180e21fa5c75f5"
  },
  {
    "url": "assets/js/56.9bee611e.js",
    "revision": "683acb2569bd87cb6d4517040407f694"
  },
  {
    "url": "assets/js/57.13010485.js",
    "revision": "04e1d60bf1498c6f4e63588c11c17493"
  },
  {
    "url": "assets/js/58.22fe855f.js",
    "revision": "8dc6b1948d80e8b73a04797758d42161"
  },
  {
    "url": "assets/js/59.1b97ada9.js",
    "revision": "b54130a82f66745d65e88d424c6819e5"
  },
  {
    "url": "assets/js/6.b71be673.js",
    "revision": "11228413bf4ceab71d2ec31eac9d9a0b"
  },
  {
    "url": "assets/js/60.b437e381.js",
    "revision": "73d4df0ac5793085c71b317ac9792355"
  },
  {
    "url": "assets/js/61.000bb45b.js",
    "revision": "3836c93e29723cfa94ea145a789ce317"
  },
  {
    "url": "assets/js/62.5c227a5f.js",
    "revision": "f3c43510c98e417bbc5d82d8ffc1903b"
  },
  {
    "url": "assets/js/63.f1d1decd.js",
    "revision": "b9aae3384cbe3a5dffcc8f1664c3598d"
  },
  {
    "url": "assets/js/64.1d213c14.js",
    "revision": "51bddd0118a3614a037ff0919cf38c1b"
  },
  {
    "url": "assets/js/65.af3951ae.js",
    "revision": "deaf142cfc332fba6dd4024eac3f5317"
  },
  {
    "url": "assets/js/66.e6759aa7.js",
    "revision": "49ee7681b10a942ff586f2b43ba1e2be"
  },
  {
    "url": "assets/js/67.7ae4e1a4.js",
    "revision": "62cc4a2d967f7d14d2f9f5aa336b8ece"
  },
  {
    "url": "assets/js/68.2d01b58a.js",
    "revision": "0edf3ad81d40de438802ff6ad69ec23b"
  },
  {
    "url": "assets/js/69.74fab142.js",
    "revision": "dac98752f85f37320ce52f37e5ed5fb2"
  },
  {
    "url": "assets/js/7.52d06c1f.js",
    "revision": "2f2a393ed87b72a49c819c259b398d1f"
  },
  {
    "url": "assets/js/70.0c38d750.js",
    "revision": "8ac292228f2e107a53cb7200966b698d"
  },
  {
    "url": "assets/js/71.a324fb52.js",
    "revision": "8caeea2d19096c66c7e41a241823d1ea"
  },
  {
    "url": "assets/js/72.8614eafe.js",
    "revision": "3ad9fe8dcc434afcc8d98446c825cfe8"
  },
  {
    "url": "assets/js/73.f2657d70.js",
    "revision": "a255546cc8741c06689774a39f2bade5"
  },
  {
    "url": "assets/js/74.690e0c24.js",
    "revision": "8cc656d8929728692c8acd339de0bbd6"
  },
  {
    "url": "assets/js/75.a0ba0dec.js",
    "revision": "8c07c6e7f352e07957b3288216c75a4b"
  },
  {
    "url": "assets/js/76.4a1b416f.js",
    "revision": "b59955cacc600a5597531f283c02a270"
  },
  {
    "url": "assets/js/77.21eae8bc.js",
    "revision": "b462c9d0df5888ca461f8f07fea14b4c"
  },
  {
    "url": "assets/js/78.8acffd35.js",
    "revision": "5ad921ccc1e2030d78721b8450e97a3f"
  },
  {
    "url": "assets/js/79.c6577150.js",
    "revision": "a1b3fc585bba9ee79bac20779ffc9b71"
  },
  {
    "url": "assets/js/8.6151909e.js",
    "revision": "36067ca3f868a72e6f3ae43c93068b2a"
  },
  {
    "url": "assets/js/80.8b4c9ded.js",
    "revision": "4bea54c5c7ac60006361d848b4f5dd43"
  },
  {
    "url": "assets/js/81.cbedde51.js",
    "revision": "eaa0f0558d8fb583c0029e69256f470e"
  },
  {
    "url": "assets/js/82.59db3eee.js",
    "revision": "8d0af523a40b9a28f60edbc3b288389e"
  },
  {
    "url": "assets/js/83.7aeb12ab.js",
    "revision": "eb5b2ea30c438ae5cac52c34a23175af"
  },
  {
    "url": "assets/js/84.33ea6031.js",
    "revision": "b99f10a135ea79235be30102dafb387b"
  },
  {
    "url": "assets/js/85.7d42f1c9.js",
    "revision": "36396052a54416fdfa16757fec141a13"
  },
  {
    "url": "assets/js/86.25badb44.js",
    "revision": "f6587bf0977bc50b079e92e213a44346"
  },
  {
    "url": "assets/js/87.1719e711.js",
    "revision": "fb9e2e575a7c9c8851d9b2b94551c01e"
  },
  {
    "url": "assets/js/88.00a3eb27.js",
    "revision": "b5295736781198d1485ef3ce503f2b6d"
  },
  {
    "url": "assets/js/89.8e1317aa.js",
    "revision": "9f745a03893154c7cff0ac97ef89f84d"
  },
  {
    "url": "assets/js/9.14e118d4.js",
    "revision": "4254442a7955b807563e215e41c18e18"
  },
  {
    "url": "assets/js/90.51442c94.js",
    "revision": "f7050e28fbd8562e4f0c7dc3e19efddc"
  },
  {
    "url": "assets/js/91.9fae46d4.js",
    "revision": "3f43a3d24d8875f1b180c390461fb89a"
  },
  {
    "url": "assets/js/92.c1a4238a.js",
    "revision": "63cc1ce7dd2b9deabb9283d0c0c91f15"
  },
  {
    "url": "assets/js/93.993a08c1.js",
    "revision": "9f9a6523180d73135cfe9eb2adb08d36"
  },
  {
    "url": "assets/js/94.3272a0ba.js",
    "revision": "30050844a859fc7792e4eb9a9658c5f4"
  },
  {
    "url": "assets/js/95.1357f495.js",
    "revision": "ea8d64f735e84c142728900f9cc00d7a"
  },
  {
    "url": "assets/js/96.062fc3a3.js",
    "revision": "133b5c8db1d65abf8d5e09c64180af94"
  },
  {
    "url": "assets/js/97.796cb487.js",
    "revision": "d9ecac923a4e546fc1f5d3747397b620"
  },
  {
    "url": "assets/js/98.7cad210d.js",
    "revision": "e60b52b58c0a10edfa4aa020fa56a745"
  },
  {
    "url": "assets/js/99.a7be163d.js",
    "revision": "54a69b2cfd969ce576169c8cf054ae43"
  },
  {
    "url": "assets/js/app.b8f3f08a.js",
    "revision": "95a4b7535e81f3dd774acf9c80c59d80"
  },
  {
    "url": "changelog.html",
    "revision": "b6cccc5cb847c705a20aecdffdf41880"
  },
  {
    "url": "guide/basic-configuration.html",
    "revision": "9cee822c78e9277666940a8b0a11c1fa"
  },
  {
    "url": "guide/creating-a-handler.html",
    "revision": "a1907b55b47dd218f1d01af614b686f6"
  },
  {
    "url": "guide/creating-a-matcher.html",
    "revision": "5d3ac3175eb29328ed4353cd50df59d0"
  },
  {
    "url": "guide/creating-a-plugin.html",
    "revision": "e1182bd17c44aa4a279db136d5465210"
  },
  {
    "url": "guide/creating-a-project.html",
    "revision": "94e8eb6dbff84f302b9fbec333f9bdd8"
  },
  {
    "url": "guide/end-or-start.html",
    "revision": "fd05f07bfaf6ff0bf89b1b8af79f1a18"
  },
  {
    "url": "guide/getting-started.html",
    "revision": "320ff4d05e65b705dc9debe2e05d052c"
  },
  {
    "url": "guide/index.html",
    "revision": "c588c3cfc42fe46d56a13673b0cf1f12"
  },
  {
    "url": "guide/installation.html",
    "revision": "fb9dcb51b4c42290261ad1820749e2fe"
  },
  {
    "url": "guide/loading-a-plugin.html",
    "revision": "8ef4be7077e3f1ec902e4e93a254cfcc"
  },
  {
    "url": "icons/android-chrome-192x192.png",
    "revision": "36b48f1887823be77c6a7656435e3e07"
  },
  {
    "url": "icons/android-chrome-384x384.png",
    "revision": "e0dc7c6250bd5072e055287fc621290b"
  },
  {
    "url": "icons/apple-touch-icon-180x180.png",
    "revision": "b8d652dd0e29786cc95c37f8ddc238de"
  },
  {
    "url": "icons/favicon-16x16.png",
    "revision": "e6c309ee1ea59d3fb1ee0582c1a7f78d"
  },
  {
    "url": "icons/favicon-32x32.png",
    "revision": "d42193f7a38ef14edb19feef8e055edc"
  },
  {
    "url": "icons/mstile-150x150.png",
    "revision": "a76847a12740d7066f602a3e627ec8c3"
  },
  {
    "url": "icons/safari-pinned-tab.svg",
    "revision": "18f1a1363394632fa5fabf95875459ab"
  },
  {
    "url": "index.html",
    "revision": "65f21a850edecac22d74f1d766201c4b"
  },
  {
    "url": "logo.png",
    "revision": "2a63bac044dffd4d8b6c67f87e1c2a85"
  },
  {
    "url": "next/advanced/export-and-require.html",
    "revision": "61ca85e977901804876054ee12b0bdcb"
  },
  {
    "url": "next/advanced/index.html",
    "revision": "7a6ec09b5b40f2992a7c4a697c6f72c3"
  },
  {
    "url": "next/advanced/permission.html",
    "revision": "b7856da33ec716d3e30be3c1c9a53c52"
  },
  {
    "url": "next/advanced/publish-plugin.html",
    "revision": "19bd08de291b0ba452b8bd722a5a822c"
  },
  {
    "url": "next/advanced/runtime-hook.html",
    "revision": "8e7b62da9d115a4e19c7d28aa7a47058"
  },
  {
    "url": "next/advanced/scheduler.html",
    "revision": "8ccb852d7f305c451b0229f9cc495247"
  },
  {
    "url": "next/api/adapters/cqhttp.html",
    "revision": "ae764b9c876b9dbb87ce710f467ed8ee"
  },
  {
    "url": "next/api/adapters/ding.html",
    "revision": "2b145915f972862de5743cbbfc128c21"
  },
  {
    "url": "next/api/adapters/index.html",
    "revision": "5b52fef8ea0226ef28689efd52e3047a"
  },
  {
    "url": "next/api/config.html",
    "revision": "75082d271077bb098af475225c502b5b"
  },
  {
    "url": "next/api/drivers/fastapi.html",
    "revision": "cab021360658049c4f20ecc2beeaee76"
  },
  {
    "url": "next/api/drivers/index.html",
    "revision": "a9707dce5081552e671bec8465cdc2d0"
  },
  {
    "url": "next/api/exception.html",
    "revision": "ce4040bad669d97d7769d80966a3d30e"
  },
  {
    "url": "next/api/index.html",
    "revision": "2f9f979ab897d641a52602fc73125226"
  },
  {
    "url": "next/api/log.html",
    "revision": "e82f15d6dd17caa36dfce18ae1966e81"
  },
  {
    "url": "next/api/matcher.html",
    "revision": "f6c552984114a062e62717edc8b95ab9"
  },
  {
    "url": "next/api/message.html",
    "revision": "0a6a6ad7dbf559eac860a71c84a0c01a"
  },
  {
    "url": "next/api/nonebot.html",
    "revision": "d17fbf6d71b076e5dfc43640a9b388b1"
  },
  {
    "url": "next/api/permission.html",
    "revision": "699067cee9990c7c55f6772c349d363f"
  },
  {
    "url": "next/api/plugin.html",
    "revision": "29143ba8ed4a8eab53ab5993c9b3d9c4"
  },
  {
    "url": "next/api/rule.html",
    "revision": "04f85f917f7f090e346c49559bb4823b"
  },
  {
    "url": "next/api/typing.html",
    "revision": "77981ffc673c456cc2f1dde0f2068649"
  },
  {
    "url": "next/api/utils.html",
    "revision": "b0672265a3387d739da45009de0dfd2a"
  },
  {
    "url": "next/guide/basic-configuration.html",
    "revision": "b7c62c37737df77da52611ed4f0ce0f6"
  },
  {
    "url": "next/guide/creating-a-handler.html",
    "revision": "a513cd949b429fd6b78d9f124c630f1f"
  },
  {
    "url": "next/guide/creating-a-matcher.html",
    "revision": "91f95df92a2b0d5383d50287f4d80425"
  },
  {
    "url": "next/guide/creating-a-plugin.html",
    "revision": "2615df8b2ce22ad27bd2fce6c3a6c63e"
  },
  {
    "url": "next/guide/creating-a-project.html",
    "revision": "cbfa30c403a757cfaec350b2d2bd9507"
  },
  {
    "url": "next/guide/end-or-start.html",
    "revision": "14fbe1c1a4bcded845217ff185702d07"
  },
  {
    "url": "next/guide/getting-started.html",
    "revision": "7221bcc42d7247795ede3622763bc930"
  },
  {
    "url": "next/guide/index.html",
    "revision": "86bf0db4c18ffafd8ba2e64dd60beda3"
  },
  {
    "url": "next/guide/installation.html",
    "revision": "f1faa724fe152953bcd191dd762a5c6a"
  },
  {
    "url": "next/guide/loading-a-plugin.html",
    "revision": "2601e650c471fbe8a5618a0e9f10515a"
  },
  {
    "url": "next/index.html",
    "revision": "c886d7df9ae5f4cd60cda8f6ed678121"
  },
  {
    "url": "plugin-store.html",
    "revision": "3875270c66a8d874490c362544b4dcc8"
  }
].concat(self.__precacheManifest || []);
workbox.precaching.precacheAndRoute(self.__precacheManifest, {});
addEventListener('message', event => {
  const replyPort = event.ports[0]
  const message = event.data
  if (replyPort && message && message.type === 'skip-waiting') {
    event.waitUntil(
      self.skipWaiting().then(
        () => replyPort.postMessage({ error: null }),
        error => replyPort.postMessage({ error })
      )
    )
  }
})
