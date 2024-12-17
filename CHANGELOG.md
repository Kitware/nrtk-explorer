# CHANGELOG



## v0.7.0 (2024-12-17)

### Chore

* chore(ci): on push to release, run semantic-release

Automatically merge release commit back to main.

Delete sync_branches workflow which was erroneously merging
back to main from release before semantic-release was run. ([`b5aa743`](https://github.com/Kitware/nrtk-explorer/commit/b5aa74320ff4e8fc7886774556b9afac3cfb3dfb))

* chore(pyproject.toml): limit nrtk to 0.16.0 ([`c8285cb`](https://github.com/Kitware/nrtk-explorer/commit/c8285cbc3403db223e61ab465a995292d211a172))

### Feature

* feat(core): add Engine kwargs alternative to cli args ([`2eb3d0d`](https://github.com/Kitware/nrtk-explorer/commit/2eb3d0d2acea774d887a59951142a5430108912b))

### Fix

* fix(dataset): load local hugging face dataset ([`9ca54f6`](https://github.com/Kitware/nrtk-explorer/commit/9ca54f67404c91d5846b21ac27fb2a72262738a2))

### Unknown

* Merge pull request #160 from Kitware/main

cut 0.7.0 ([`6e6ab8a`](https://github.com/Kitware/nrtk-explorer/commit/6e6ab8aec7654742401ec84a34e81d9243ba96d7))

* Merge pull request #158 from Kitware/kwargs-config

Engine kwargs as alternative to CLI args ([`ed1e971`](https://github.com/Kitware/nrtk-explorer/commit/ed1e9716bc00e79902a47076bc310e5504365768))

* Merge pull request #154 from Kitware/release

0.6.0 ([`a0dc46e`](https://github.com/Kitware/nrtk-explorer/commit/a0dc46e2b7e4012f6bd6f039a12b82a9b4b0ce89))


## v0.6.0 (2024-12-12)

### Chore

* chore(pyproject.toml): set trame-annotations min to 0.4.0 ([`b45bf2c`](https://github.com/Kitware/nrtk-explorer/commit/b45bf2c4b605d90d8bf0f2bd0db041dec24d871d))

### Documentation

* docs(nebari): describe and test nebari setup ([`227b65d`](https://github.com/Kitware/nrtk-explorer/commit/227b65d447d6abb21ca9a41ab874a2a846c87bad))

### Feature

* feat: add confidence score threshold ([`b75b50c`](https://github.com/Kitware/nrtk-explorer/commit/b75b50c30fcc008a39e2c133c914b4fb8b666632))

* feat(stateful_annotations): put annotation score on state ([`e2366a8`](https://github.com/Kitware/nrtk-explorer/commit/e2366a854ff8afc73fffb3a219063657c43dad67))

* feat(coco_utils): add scoring for classification model ([`32660f6`](https://github.com/Kitware/nrtk-explorer/commit/32660f63be4e76b4705b5f9c9c60d576cdc2e118))

* feat(stateful_annotations): support non bbox predictions ([`be88218`](https://github.com/Kitware/nrtk-explorer/commit/be88218b233cf4e5620be85c108dfd9cfc919271))

* feat: support classification datasets ([`5428c1c`](https://github.com/Kitware/nrtk-explorer/commit/5428c1c0428abf18fbac6d01bb036b7761e8bb8d))

* feat(transforms): add ability to add multiple transforms ([`3d58599`](https://github.com/Kitware/nrtk-explorer/commit/3d585998f2c7c7a23333a1e242a59b00c8c8f295))

* feat(dataset): add download CLI argument for HF datasets

Defaulting to streaming download for HF datasets, but now you can specify
`--download` to download the dataset to disk before loading it. ([`f3a84e1`](https://github.com/Kitware/nrtk-explorer/commit/f3a84e13e9fca345a9f1bbf7436db74452c2c7b3))

* feat(dataset): add streaming option to HF datasets ([`1818745`](https://github.com/Kitware/nrtk-explorer/commit/18187454b9a9c19216831d9345daa55d6582e9a1))

* feat(dataset): expand HF dataset splits as new datasets ([`c613029`](https://github.com/Kitware/nrtk-explorer/commit/c61302916d78ad0491a3202f0d1f6b54dbcd6add))

* feat(dataset): load hugging face datasets

Wraps a HF dataset into our Coco like dataset API. ([`3344920`](https://github.com/Kitware/nrtk-explorer/commit/3344920d32c702fe6d5c5af8a60cf8902bcc8989))

* feat(transforms): add CLI arg for inference models ([`9f4a5e0`](https://github.com/Kitware/nrtk-explorer/commit/9f4a5e03e0b981eed99dcb470b10667cf5820151))

* feat(ImageDetection): use component from trame-annotations ([`c4cecc6`](https://github.com/Kitware/nrtk-explorer/commit/c4cecc68a7fad656c1dad19587c808ddad2bb068))

### Fix

* fix(pyproject): avoid broken pybsm version

Also update scikit-learn

closes #150 ([`c914e6c`](https://github.com/Kitware/nrtk-explorer/commit/c914e6cb36b46b44ad5c35c57b726478f29049f4))

* fix(images): avoid OSError - to many open files

Closes #145 ([`fd8d43d`](https://github.com/Kitware/nrtk-explorer/commit/fd8d43d991ea54a6a4e8e9074144f3be39f577d2))

* fix(dataset): add types ([`d24e9e5`](https://github.com/Kitware/nrtk-explorer/commit/d24e9e5f400be26ad06fc16ba035412e93ec9de3))

* fix(dataset): add get_image to KWCocoDataset ([`389403d`](https://github.com/Kitware/nrtk-explorer/commit/389403dc21557796980baac8994bfe446f23fa75))

* fix(dataset): support list/row first datasets ([`6c9567b`](https://github.com/Kitware/nrtk-explorer/commit/6c9567b4d0e49725fec7858c1b322b01005fc82c))

* fix(dataset): transforms require RGB mode images ([`5c176d7`](https://github.com/Kitware/nrtk-explorer/commit/5c176d7d6fa84972582a600c0c9b2121f0881d75))

* fix(dataset): less picky about dataset feature shape ([`9983b21`](https://github.com/Kitware/nrtk-explorer/commit/9983b2161ec0aec0aea60bf41d310f2011b93de8))

* fix(dataset): support more HF datasets

* Fix converting CMYK image formats to PNG.
* Remove use of get_image_fpath in app. ([`261191e`](https://github.com/Kitware/nrtk-explorer/commit/261191e7e44a2631589c27d0bbf7b637c60d9ea1))

### Performance

* perf(dataset): convert image mode to RGB on HF dataset load ([`752b56f`](https://github.com/Kitware/nrtk-explorer/commit/752b56ff47d2abfa102e654ba4c5197fbe12a314))

* perf(dataset): loop through dataset once ([`a451b97`](https://github.com/Kitware/nrtk-explorer/commit/a451b970392e697537160ce52f5acc91063218a2))

### Refactor

* refactor: add annotations lib module ([`f3b76c4`](https://github.com/Kitware/nrtk-explorer/commit/f3b76c4029a39e3d9f02586815817443abe6ade8))

* refactor: rename object_detection_model to inference_model ([`ca3f7b4`](https://github.com/Kitware/nrtk-explorer/commit/ca3f7b4c609e16688c639043e69bbfcf4a9db7c4))

* refactor(coco_utils): make normalized annotation struct ([`ae6279e`](https://github.com/Kitware/nrtk-explorer/commit/ae6279eb95b28a57ef879c1d4a4dd712826dfbf7))

* refactor(transforms): move score logic to coco_utils ([`b61bd34`](https://github.com/Kitware/nrtk-explorer/commit/b61bd349b574ac625224ab03ba249583e3b0be06))

* refactor(images): move img.mode(&#34;RBG&#34;) to image loader ([`be817b9`](https://github.com/Kitware/nrtk-explorer/commit/be817b96a8ffd3be77f07b8b90c8ed34f46c16aa))

* refactor(dataset): simplify extract_labels ([`9d7c2ee`](https://github.com/Kitware/nrtk-explorer/commit/9d7c2eeb3215c6adaa6b52df196d945e974f3bb7))

* refactor(dataset): share common code between dataset classes ([`6b6b381`](https://github.com/Kitware/nrtk-explorer/commit/6b6b381eccd5b8ac4d1f6f0b2b4853fd53e25e5e))

* refactor(dataset): rename JsonDataset ([`7d4022b`](https://github.com/Kitware/nrtk-explorer/commit/7d4022b09cf66617aca5d353f69826c47dbec0c9))

* refactor(transforms): fix spelling visibile -&gt; visible ([`d2fd39d`](https://github.com/Kitware/nrtk-explorer/commit/d2fd39dc64dbac07a3a2038526197cdf81b2cae8))

### Unknown

* Merge release into main ([`3288fe2`](https://github.com/Kitware/nrtk-explorer/commit/3288fe2e6c67bb76d7521b1a978b92fac08bf1f9))

* Merge pull request #153 from Kitware/main

Cut PiPy 0.6.0 release ([`a1df9a5`](https://github.com/Kitware/nrtk-explorer/commit/a1df9a5a0c31c3d3b14f1755845c92a4863b77bb))

* doc(README): add HF dataset CLI arg and more usage examples ([`38393e1`](https://github.com/Kitware/nrtk-explorer/commit/38393e1109dd054904fde466b458e8cfed609fc0))

* Add a wide variety of nrtk transforms (PIL, cv2, skimage, pybsm) ([`b5ca99c`](https://github.com/Kitware/nrtk-explorer/commit/b5ca99c3e909d134982a2bb98717f64c218329b7))


## v0.5.0 (2024-10-21)

### Ci

* ci: type checking ([`51110be`](https://github.com/Kitware/nrtk-explorer/commit/51110be2183796de6c8c0c89c66f24dac37cad9a))

### Documentation

* docs(sphinx): Precommit hooks ([`d80270c`](https://github.com/Kitware/nrtk-explorer/commit/d80270c4285f68329d027af231fabb4a1c65834b))

* docs(sphinx): Add DEVELOPMENT instructions. ([`115b272`](https://github.com/Kitware/nrtk-explorer/commit/115b272b0a7f0aaa3ed854aa9ca038662c8c25f6))

* docs(sphinx): Add sphinx auto-api docs. ([`4a4d88f`](https://github.com/Kitware/nrtk-explorer/commit/4a4d88fd8a46021bbb820b98bba648be231c9e73))

* docs(README): add back installation section ([`5b019a6`](https://github.com/Kitware/nrtk-explorer/commit/5b019a62f439d602feb72b978df7aed36628a068))

* docs(README): format style ([`79aec9a`](https://github.com/Kitware/nrtk-explorer/commit/79aec9acad35f52ad1d7bbfdbecfecc7de942106))

* docs(README): add release section, screenshot, remove install section ([`c5df7e7`](https://github.com/Kitware/nrtk-explorer/commit/c5df7e73bb0d0de55826e07f82a7a1d33ce8ea86))

### Feature

* feat(perturber): add support for loading more perturber via YAML definition ([`a58ac87`](https://github.com/Kitware/nrtk-explorer/commit/a58ac87d009bdb81181e1cd91c8ff3617c00eeea))

### Fix

* fix(trame): ensure newer version of trame to suport used API

fix #136 ([`1feb094`](https://github.com/Kitware/nrtk-explorer/commit/1feb09437997407897fb8a094fdd6d4a62df3fb7))

* fix(nrtk): update arguments to PybsmPerturber

New version of nrtk broke old sensor scenerio parameter factory we had. ([`28b3183`](https://github.com/Kitware/nrtk-explorer/commit/28b3183af84239acea0740a519cedc1896980914))

* fix(deps): add nrtk[headless] extra to fix runtime error

nrkt put opencv-python under an extra in 0.12.0 https://github.com/Kitware/nrtk/releases/tag/v0.12.0 ([`d664ad7`](https://github.com/Kitware/nrtk-explorer/commit/d664ad785748e44fdb71dbc6cc5640de751303f8))

* fix(transforms): on dataset change stop processing

Fixes key error accessing images in new dataset with old dataset image ids. ([`9fb545e`](https://github.com/Kitware/nrtk-explorer/commit/9fb545e70ce16e708117a0723583af119ce240da))

* fix(debounce): only await coroutines

fixes #130 ([`61e4e8d`](https://github.com/Kitware/nrtk-explorer/commit/61e4e8d6dfeecef6ce442a4e00ed609d25d6aefb))

### Refactor

* refactor(image-list): reuse AbstractElement state+ctrl

Guard against double call to init_visibile_columns ([`0d42b9e`](https://github.com/Kitware/nrtk-explorer/commit/0d42b9e26de97be22eca6ce1f75b89dca5c9934a))

* refactor(image-list): move in column visibility logic ([`51b9fdf`](https://github.com/Kitware/nrtk-explorer/commit/51b9fdf290cd337ee5a624e976a81f6011e48a77))

* refactor(image-list): move image_list_ids logic to ImageList class ([`538da8d`](https://github.com/Kitware/nrtk-explorer/commit/538da8da032bee6d31fa2165b75288259a6c946c))

* refactor(image-list): move pagnation state updates to class ([`c2dd051`](https://github.com/Kitware/nrtk-explorer/commit/c2dd0511e663de24090c093f97801ed7a0f1e01e))

* refactor(image-list): use TrameApp on ImageList for change decorators ([`88d446f`](https://github.com/Kitware/nrtk-explorer/commit/88d446f95156e6b077e6c53889581f473b67136d))

### Unknown

* Merge pull request #139 from Kitware/fix-dep-version

fix(trame): ensure newer version of trame to suport used API ([`1feffc5`](https://github.com/Kitware/nrtk-explorer/commit/1feffc5ac662d352458e35bec2a485be4fa77a47))

* Merge pull request #137 from Erotemic/docs

Add documentation ([`9175aa7`](https://github.com/Kitware/nrtk-explorer/commit/9175aa7875824f5f6ba624344bfbcd12f2aa8b17))

* Merge pull request #133 from Kitware/yaml-perturbators

Yaml perturbators ([`58bb073`](https://github.com/Kitware/nrtk-explorer/commit/58bb073a416ea880c780b836ce7804642448a27b))

* Merge pull request #129 from Kitware/release

0.4.0 ([`ca2baab`](https://github.com/Kitware/nrtk-explorer/commit/ca2baabb32504e477ddcd2cdeac145c5fc703ed4))

* Merge release into main ([`1c9359e`](https://github.com/Kitware/nrtk-explorer/commit/1c9359e87b4e0255ab232b32263680f8314f043f))


## v0.4.0 (2024-10-08)

### Chore

* chore(deps): update build requirement from &lt;0.10.0 to &lt;1.3.0

Updates the requirements on [build](https://github.com/pypa/build) to permit the latest version.
- [Release notes](https://github.com/pypa/build/releases)
- [Changelog](https://github.com/pypa/build/blob/main/CHANGELOG.rst)
- [Commits](https://github.com/pypa/build/compare/0.0.1...1.2.2)

---
updated-dependencies:
- dependency-name: build
  dependency-type: direct:production
...

Signed-off-by: dependabot[bot] &lt;support@github.com&gt; ([`82bf3c9`](https://github.com/Kitware/nrtk-explorer/commit/82bf3c93888206d77dc1287075cdb0711ac98a9e))

* chore(deps-dev): bump vite from 4.5.3 to 4.5.5 in /vue-components

Bumps [vite](https://github.com/vitejs/vite/tree/HEAD/packages/vite) from 4.5.3 to 4.5.5.
- [Release notes](https://github.com/vitejs/vite/releases)
- [Changelog](https://github.com/vitejs/vite/blob/v4.5.5/packages/vite/CHANGELOG.md)
- [Commits](https://github.com/vitejs/vite/commits/v4.5.5/packages/vite)

---
updated-dependencies:
- dependency-name: vite
  dependency-type: direct:development
...

Signed-off-by: dependabot[bot] &lt;support@github.com&gt; ([`d103f97`](https://github.com/Kitware/nrtk-explorer/commit/d103f9720c72807502b3e83495d81fc602bc74ad))

* chore(deps): bump rollup from 3.29.4 to 3.29.5 in /vue-components

Bumps [rollup](https://github.com/rollup/rollup) from 3.29.4 to 3.29.5.
- [Release notes](https://github.com/rollup/rollup/releases)
- [Changelog](https://github.com/rollup/rollup/blob/master/CHANGELOG.md)
- [Commits](https://github.com/rollup/rollup/compare/v3.29.4...v3.29.5)

---
updated-dependencies:
- dependency-name: rollup
  dependency-type: indirect
...

Signed-off-by: dependabot[bot] &lt;support@github.com&gt; ([`a6932ae`](https://github.com/Kitware/nrtk-explorer/commit/a6932ae862b941653e6ce6c42c6a06a8d02ec810))

* chore(docker): add docker deploy definition ([`97db133`](https://github.com/Kitware/nrtk-explorer/commit/97db13331274031bd5dad1e16ebc674af7f65013))

* chore(deps): bump scikit-learn from 1.5.1 to 1.5.2

Bumps [scikit-learn](https://github.com/scikit-learn/scikit-learn) from 1.5.1 to 1.5.2.
- [Release notes](https://github.com/scikit-learn/scikit-learn/releases)
- [Commits](https://github.com/scikit-learn/scikit-learn/compare/1.5.1...1.5.2)

---
updated-dependencies:
- dependency-name: scikit-learn
  dependency-type: direct:production
  update-type: version-update:semver-patch
...

Signed-off-by: dependabot[bot] &lt;support@github.com&gt; ([`ebace6e`](https://github.com/Kitware/nrtk-explorer/commit/ebace6e3cc21fb132faa4f1d0215f04b77db6b50))

* chore(deps): update build requirement from &lt;0.10.0 to &lt;1.3.0

Updates the requirements on [build](https://github.com/pypa/build) to permit the latest version.
- [Release notes](https://github.com/pypa/build/releases)
- [Changelog](https://github.com/pypa/build/blob/main/CHANGELOG.rst)
- [Commits](https://github.com/pypa/build/compare/0.0.1...1.2.2)

---
updated-dependencies:
- dependency-name: build
  dependency-type: direct:production
...

Signed-off-by: dependabot[bot] &lt;support@github.com&gt; ([`7f2d827`](https://github.com/Kitware/nrtk-explorer/commit/7f2d827de7fb5ed955d56af2af0681a94ea8481d))

* chore(deps-dev): bump vite from 4.5.3 to 4.5.5 in /vue-components

Bumps [vite](https://github.com/vitejs/vite/tree/HEAD/packages/vite) from 4.5.3 to 4.5.5.
- [Release notes](https://github.com/vitejs/vite/releases)
- [Changelog](https://github.com/vitejs/vite/blob/v4.5.5/packages/vite/CHANGELOG.md)
- [Commits](https://github.com/vitejs/vite/commits/v4.5.5/packages/vite)

---
updated-dependencies:
- dependency-name: vite
  dependency-type: direct:development
...

Signed-off-by: dependabot[bot] &lt;support@github.com&gt; ([`9d527c0`](https://github.com/Kitware/nrtk-explorer/commit/9d527c0f349bdd4a00d92a892bf762e1b8264d47))

* chore(deps): bump rollup from 3.29.4 to 3.29.5 in /vue-components

Bumps [rollup](https://github.com/rollup/rollup) from 3.29.4 to 3.29.5.
- [Release notes](https://github.com/rollup/rollup/releases)
- [Changelog](https://github.com/rollup/rollup/blob/master/CHANGELOG.md)
- [Commits](https://github.com/rollup/rollup/compare/v3.29.4...v3.29.5)

---
updated-dependencies:
- dependency-name: rollup
  dependency-type: indirect
...

Signed-off-by: dependabot[bot] &lt;support@github.com&gt; ([`1920493`](https://github.com/Kitware/nrtk-explorer/commit/19204939202428f9fb17ea6a6316a8b8716501ec))

* chore(docker): add docker deploy definition ([`497e390`](https://github.com/Kitware/nrtk-explorer/commit/497e39026f6646acc72e9dde3cc4c578a96fd538))

* chore(deps): bump scikit-learn from 1.5.1 to 1.5.2

Bumps [scikit-learn](https://github.com/scikit-learn/scikit-learn) from 1.5.1 to 1.5.2.
- [Release notes](https://github.com/scikit-learn/scikit-learn/releases)
- [Commits](https://github.com/scikit-learn/scikit-learn/compare/1.5.1...1.5.2)

---
updated-dependencies:
- dependency-name: scikit-learn
  dependency-type: direct:production
  update-type: version-update:semver-patch
...

Signed-off-by: dependabot[bot] &lt;support@github.com&gt; ([`eb43492`](https://github.com/Kitware/nrtk-explorer/commit/eb43492d4c12a4169c97df00f9289f78adb8dd73))

### Documentation

* docs(README): update screenshot ([`1a834f9`](https://github.com/Kitware/nrtk-explorer/commit/1a834f93779daf73b0434f931f8a04775a487956))

* docs(README): update screenshot ([`627bc08`](https://github.com/Kitware/nrtk-explorer/commit/627bc08795dae59d834398dc162daed23efb611a))

### Feature

* feat(core): default to 500 sampled dataset images ([`2e763ce`](https://github.com/Kitware/nrtk-explorer/commit/2e763ce330e52a9f8f34936958a6dcb61198af4d))

* feat(ScatterPlot): stay in selection mode after selection ([`1edd988`](https://github.com/Kitware/nrtk-explorer/commit/1edd9886cb5e1ac984eb9eeb7437d97ccc2c5b0a))

* feat(ScatterPlot): dark gray for selected points

Light gray for unselected points. Was light blue for unselected points, light gray for selected. ([`5f482c8`](https://github.com/Kitware/nrtk-explorer/commit/5f482c80a98e9e53f708c7337ccb001e642e8275))

* feat(transforms): add 3 more object detection models ([`b2f65ce`](https://github.com/Kitware/nrtk-explorer/commit/b2f65ceb3d4046b92363fff1f449d6a30b6ccbdf))

* feat(image_list): only show spinner if show annotations is on

or image is loading ([`a1a3e18`](https://github.com/Kitware/nrtk-explorer/commit/a1a3e18e845056dd2cc00be7950e2a1559f75095))

* feat(image_list): use normal switch for show annotations ([`f527fef`](https://github.com/Kitware/nrtk-explorer/commit/f527fefc23f8e098a5f5b9a6555e849d80947aa8))

* feat(image_list): add switch to hide annotations ([`12f2971`](https://github.com/Kitware/nrtk-explorer/commit/12f29719c3d892dab5dd22f958466a2a6c2f834f))

* feat(image_list): slider for image size ([`187bd66`](https://github.com/Kitware/nrtk-explorer/commit/187bd6627691baebfbf89e0c73a4b51035512274))

* feat(filtering): relabel Apply button to Select Images ([`59d9da9`](https://github.com/Kitware/nrtk-explorer/commit/59d9da9908c61cf05601527b0d273dc659a1bc59))

* feat(layout): move category filter to bottom ([`b4dec14`](https://github.com/Kitware/nrtk-explorer/commit/b4dec144d98777dec35c5d98e879b56644c95697))

* feat(transforms): toggle switch to disable object detection ([`b6cb739`](https://github.com/Kitware/nrtk-explorer/commit/b6cb739ea88ba9698dc75ca304db15b751141c30))

* feat(transforms): toggle component to disable transforms ([`0d79fca`](https://github.com/Kitware/nrtk-explorer/commit/0d79fca0278581b7aedf9c92b6f64eb69cb83ae8))

* feat(transforms): add disable transform option ([`5cd2601`](https://github.com/Kitware/nrtk-explorer/commit/5cd2601b29f4e98d85ce7e2e8048dfaad8506bd5))

* feat(core): default to 500 sampled dataset images ([`80100f0`](https://github.com/Kitware/nrtk-explorer/commit/80100f0d0c29f5e011448b63b48df67d818e6b04))

* feat(ScatterPlot): stay in selection mode after selection ([`2459642`](https://github.com/Kitware/nrtk-explorer/commit/24596425188bfa9a0e66330982688db1ba8cf1cf))

* feat(ScatterPlot): dark gray for selected points

Light gray for unselected points. Was light blue for unselected points, light gray for selected. ([`2391c3e`](https://github.com/Kitware/nrtk-explorer/commit/2391c3e3c37bc5422c796d2a3f0aabbf18f318b7))

* feat(transforms): add 3 more object detection models ([`f8f524f`](https://github.com/Kitware/nrtk-explorer/commit/f8f524fb18455bf3b2c0d14d5f5f9dacb4cef5c3))

* feat(image_list): only show spinner if show annotations is on

or image is loading ([`3bedfd0`](https://github.com/Kitware/nrtk-explorer/commit/3bedfd00bd7f670bd063f631e23d4f90ea756f33))

* feat(image_list): use normal switch for show annotations ([`a910f28`](https://github.com/Kitware/nrtk-explorer/commit/a910f288f3fded95c9fbc269f195c44cd13bd90a))

* feat(image_list): add switch to hide annotations ([`fc201fc`](https://github.com/Kitware/nrtk-explorer/commit/fc201fcf517f9df1699976ef5591f2726e8d2760))

* feat(image_list): slider for image size ([`e6a2957`](https://github.com/Kitware/nrtk-explorer/commit/e6a295757f5ec5f376bc424820654be3eac45ea7))

* feat(filtering): relabel Apply button to Select Images ([`829877f`](https://github.com/Kitware/nrtk-explorer/commit/829877fd9962e3699793cf9013126efe79b6d68b))

* feat(layout): move category filter to bottom ([`a7b5a94`](https://github.com/Kitware/nrtk-explorer/commit/a7b5a94bd0851eab18d77537e461d927cfb7c1e1))

* feat(transforms): toggle switch to disable object detection ([`8846751`](https://github.com/Kitware/nrtk-explorer/commit/884675113ce8de099ab93adc905f2d55dc7793e7))

* feat(transforms): toggle component to disable transforms ([`3707bad`](https://github.com/Kitware/nrtk-explorer/commit/3707badb31a36b4ad9c9a58ab69eacf77266e3dd))

* feat(transforms): add disable transform option ([`97594f1`](https://github.com/Kitware/nrtk-explorer/commit/97594f1275d1b782d7432052ff84e259e05b8685))

### Fix

* fix(ImageDetection): stop tooltip overflow with fudge to center ([`437b6a5`](https://github.com/Kitware/nrtk-explorer/commit/437b6a557221db6808a9fac0a6296ce30172dc50))

* fix(core): dataset path does not overflow select dropdown ([`b33b975`](https://github.com/Kitware/nrtk-explorer/commit/b33b9758fb990f1a874d1eccc3933b4b0e54c78b))

* fix(ScatterPlot): reactive color map control and perf

Big performance improvements for many point ([`6197f16`](https://github.com/Kitware/nrtk-explorer/commit/6197f16762ffcefa89f52676a102d890b396964a))

* fix(embeddings): disable transforms switch hides points

closes #113 ([`2a6768a`](https://github.com/Kitware/nrtk-explorer/commit/2a6768a82916d58271d9c02110a0ccf458c70cc0))

* fix(images): dont remove image from cache for embeddings ([`e0afacd`](https://github.com/Kitware/nrtk-explorer/commit/e0afacda35b0c43f94fa0b5e88bb1d0b525e3906))

* fix(transforms): turn on transform enabled switch on apply button ([`c821022`](https://github.com/Kitware/nrtk-explorer/commit/c82102255561318d7b6654137c33a858e7e9b0e3))

* fix(dep): properly describe expected version ([`d3c060b`](https://github.com/Kitware/nrtk-explorer/commit/d3c060ba5877d815addc7be4118ee281e3d5dc72))

* fix(network): ensure network completion before heavy work ([`26c73c0`](https://github.com/Kitware/nrtk-explorer/commit/26c73c026e2e4d81bf8dd43126636731100619c2))

* fix(ui): use class components ([`5fafd29`](https://github.com/Kitware/nrtk-explorer/commit/5fafd291376d3c284fab9400e91368e91a03544a))

* fix(embeddings): dont send empty lists to dim reducer ([`ce24374`](https://github.com/Kitware/nrtk-explorer/commit/ce24374291741af667832e72f52ffa8f539c80ee))

* fix(embedding): attempt to revive standalone mode ([`a68d917`](https://github.com/Kitware/nrtk-explorer/commit/a68d917ca6e8b804e92e08df9adab7f4ed0e7850))

* fix(embedding): standalone mode works again ([`f577e99`](https://github.com/Kitware/nrtk-explorer/commit/f577e992f705d0956d166c7d39063fa0b0a53867))

* fix(project): cleanup dependency structure ([`6f64c10`](https://github.com/Kitware/nrtk-explorer/commit/6f64c10ff64c7135c5cecc4863ec58d273384685))

* fix(ImageDetection): stop tooltip overflow with fudge to center ([`0346cfc`](https://github.com/Kitware/nrtk-explorer/commit/0346cfcce1dcc50438aaf42795bf94bb0ed50cd5))

* fix(core): dataset path does not overflow select dropdown ([`98c05a6`](https://github.com/Kitware/nrtk-explorer/commit/98c05a684896f5756849cf45a8cb90bb02c446ae))

* fix(ScatterPlot): reactive color map control and perf

Big performance improvements for many point ([`3b1e1db`](https://github.com/Kitware/nrtk-explorer/commit/3b1e1dba493edb0a10572f4e1fa5057300f0ac35))

* fix(embeddings): disable transforms switch hides points

closes #113 ([`f624be7`](https://github.com/Kitware/nrtk-explorer/commit/f624be7d7741b72b6cb050c8dfe7ea9749764d29))

* fix(images): dont remove image from cache for embeddings ([`9a30492`](https://github.com/Kitware/nrtk-explorer/commit/9a30492f48864c8e1611381169d6affe11d7683c))

* fix(transforms): turn on transform enabled switch on apply button ([`e11c986`](https://github.com/Kitware/nrtk-explorer/commit/e11c986e432be6309ca0b1dbbaea6b5fad0a8b70))

* fix(dep): properly describe expected version ([`f106a3e`](https://github.com/Kitware/nrtk-explorer/commit/f106a3e3a6f93127e5b2fac6a473162ff4d72ff4))

* fix(network): ensure network completion before heavy work ([`997626a`](https://github.com/Kitware/nrtk-explorer/commit/997626aac82af59929de53312b5704fd7ab1f41b))

* fix(ui): use class components ([`1f059f9`](https://github.com/Kitware/nrtk-explorer/commit/1f059f990715b3023142a3bbf2a9f5ae72d8b98c))

* fix(embeddings): dont send empty lists to dim reducer ([`6663efd`](https://github.com/Kitware/nrtk-explorer/commit/6663efd2aff7a2f8a4c34428163d9f2ae712ee93))

* fix(embedding): attempt to revive standalone mode ([`ef49bd9`](https://github.com/Kitware/nrtk-explorer/commit/ef49bd955199815e17e4ee2a20efae2c1a313c19))

* fix(embedding): standalone mode works again ([`f30a5fb`](https://github.com/Kitware/nrtk-explorer/commit/f30a5fba03af9cd9e8423adcc46f29a721a49b47))

* fix(project): cleanup dependency structure ([`f67fc38`](https://github.com/Kitware/nrtk-explorer/commit/f67fc388b539ff8a1cce0374f7a0728d35f0abe1))

### Performance

* perf(core): add debounce to sample size slider

Closes #115 ([`c841024`](https://github.com/Kitware/nrtk-explorer/commit/c841024d47080de8438f9dd909357a591fd70ba4))

* perf(images): add cache backed get_stateful_image funcs

Sometimes we don&#39;t need the image for visualization and don&#39;t
need to put it on the trame state. ([`356c78a`](https://github.com/Kitware/nrtk-explorer/commit/356c78a64ba95f9d8d5882a0af40509d554e7c58))

* perf(core): add debounce to sample size slider

Closes #115 ([`5676a1f`](https://github.com/Kitware/nrtk-explorer/commit/5676a1f4f7d765c59755e9f22026360944f55c9c))

* perf(images): add cache backed get_stateful_image funcs

Sometimes we don&#39;t need the image for visualization and don&#39;t
need to put it on the trame state. ([`cf93436`](https://github.com/Kitware/nrtk-explorer/commit/cf93436df742aae3f15ad1bd239279e0d1b7182a))

### Refactor

* refactor(annotations): reuse LruCache for annotations ([`3f5f704`](https://github.com/Kitware/nrtk-explorer/commit/3f5f70451ee759c6d0ad60386cd5f3fca45ef010))

* refactor(images): move module level funcs to class ([`3d306e6`](https://github.com/Kitware/nrtk-explorer/commit/3d306e66f465fcd9d4694038809308fc9af93454))

* refactor(transforms): extract detection and transform enable/disable logic ([`a6252fa`](https://github.com/Kitware/nrtk-explorer/commit/a6252fa4356cc9f76af708b27817b9b8b2537238))

* refactor(annotations): reuse LruCache for annotations ([`d2070bf`](https://github.com/Kitware/nrtk-explorer/commit/d2070bfb46260078682ace4e0888827174c54cb2))

* refactor(images): move module level funcs to class ([`8291cb2`](https://github.com/Kitware/nrtk-explorer/commit/8291cb2e8aabf9328c11f28af0e5270356fe0c11))

* refactor(transforms): extract detection and transform enable/disable logic ([`6e0573a`](https://github.com/Kitware/nrtk-explorer/commit/6e0573a5afed1ca31daee7f38d86ff4697e6a4ef))

### Unknown

* All sampled images in image list (#88)

* feat: show all images in list

* feat(embeddings): selection of points filters list

* refactor(object_detector): remove images_manager dependency

* refactor: move image modules into images folder

* refactor: use BufferCache for images

* refactor: use BufferCache for annotations

* refactor: clean dead code

* fix(embeddings): add transformed img point as computed

* chore(ci): run tests without depending on linters

* fix(image_list): respect client side sorting and filtering

* fix(ScatterPlot): correct is_transformed in hover

* fix(image_list): paginate grid view

Grid view does not do virtual scrolling

* perf(object_detector): reuse last successful batch size

* refactor: remove images_manager

* fix: flush transformed images to state before detection

* fix(images): actually call on_clear callback in BufferCache

* feat(image_list): hide dependant columns when transforms disabled

* refactor(images): use lru_cache for image functions

* refactor(ScatterPlot): rename props to use points

ScatterPlot could be used for non images data.

* refactor: reorder images.py and doc object_detector

* refactor(annotations): move logic from images.py ([`9850cf6`](https://github.com/Kitware/nrtk-explorer/commit/9850cf6118b1bdd04117b2f79dee9d375ee3ff8c))

* Merge pull request #110 from Kitware/dependabot/pip/scikit-learn-1.5.2

chore(deps): bump scikit-learn from 1.5.1 to 1.5.2 ([`210d91f`](https://github.com/Kitware/nrtk-explorer/commit/210d91fe500f870e902152ce9bfab826aae0a357))

* Merge pull request #120 from Kitware/dependabot/npm_and_yarn/vue-components/rollup-3.29.5

chore(deps): bump rollup from 3.29.4 to 3.29.5 in /vue-components ([`af3cab5`](https://github.com/Kitware/nrtk-explorer/commit/af3cab5627a0a798ef4706482e866d4db3ee5e19))

* Merge pull request #121 from Kitware/dependabot/npm_and_yarn/vue-components/vite-4.5.5

chore(deps-dev): bump vite from 4.5.3 to 4.5.5 in /vue-components ([`9893897`](https://github.com/Kitware/nrtk-explorer/commit/989389712e5f0465d7179a198226d3acbe30f744))

* Merge pull request #109 from Kitware/better-network-wait

Better network wait ([`424ff36`](https://github.com/Kitware/nrtk-explorer/commit/424ff369d96be1b48bb63ed85e4356964135fbfa))

* All sampled images in image list (#88)

* feat: show all images in list

* feat(embeddings): selection of points filters list

* refactor(object_detector): remove images_manager dependency

* refactor: move image modules into images folder

* refactor: use BufferCache for images

* refactor: use BufferCache for annotations

* refactor: clean dead code

* fix(embeddings): add transformed img point as computed

* chore(ci): run tests without depending on linters

* fix(image_list): respect client side sorting and filtering

* fix(ScatterPlot): correct is_transformed in hover

* fix(image_list): paginate grid view

Grid view does not do virtual scrolling

* perf(object_detector): reuse last successful batch size

* refactor: remove images_manager

* fix: flush transformed images to state before detection

* fix(images): actually call on_clear callback in BufferCache

* feat(image_list): hide dependant columns when transforms disabled

* refactor(images): use lru_cache for image functions

* refactor(ScatterPlot): rename props to use points

ScatterPlot could be used for non images data.

* refactor: reorder images.py and doc object_detector

* refactor(annotations): move logic from images.py ([`421ca9b`](https://github.com/Kitware/nrtk-explorer/commit/421ca9b56e38fb47022d103cba7b5e8c30814453))


## v0.3.2 (2024-08-30)

### Ci

* ci: add noop release check ([`1a48185`](https://github.com/Kitware/nrtk-explorer/commit/1a481853af9691ca185261d0c580ca1cb7e51ca2))

* ci: set make_release as manual job ([`0fb5fa2`](https://github.com/Kitware/nrtk-explorer/commit/0fb5fa2351b64587c1cb2480326a41b55883dcda))

* ci: add sync job ([`7962ee3`](https://github.com/Kitware/nrtk-explorer/commit/7962ee3be0c8530101d22ddb6178945189e59011))

### Fix

* fix(dataset): set kwcoco optional backend ([`7400518`](https://github.com/Kitware/nrtk-explorer/commit/74005184f9530b3ac5c48da2f53023a92c1fee45))

* fix(transforms): parametrize pybsm darkCurrentFromDensity call ([`af34dbb`](https://github.com/Kitware/nrtk-explorer/commit/af34dbbcb80c95ee2bbc1dea3bfd42c4aa4aba8d))

### Unknown

* Merge pull request #101 from Kitware/main

Bring master changes ([`9c87f92`](https://github.com/Kitware/nrtk-explorer/commit/9c87f92e4eecee5199fec85ed8b04812e9c5ae04))

* conda: add conda env that includes cuda pytorch ([`e5f0b41`](https://github.com/Kitware/nrtk-explorer/commit/e5f0b41842399d5cf6f57267f0b236a19e344e61))

* Merge release into main ([`f0a1884`](https://github.com/Kitware/nrtk-explorer/commit/f0a1884e6827ca0ed0ccfad7ea0837df4eaa5df4))

* Merge branch &#39;main&#39; into release

* main:
  ci: set make_release as manual job
  ci: add sync job ([`d0a9b37`](https://github.com/Kitware/nrtk-explorer/commit/d0a9b37eb28e4e334352ede0f19416fde7d719ad))

* Auto-merge release back to main ([`e4b4eeb`](https://github.com/Kitware/nrtk-explorer/commit/e4b4eeb9383f0557b9664981b9ae5dae1012d36b))


## v0.3.1 (2024-08-26)

### Ci

* ci: add manual trigger create release build ([`f5c577c`](https://github.com/Kitware/nrtk-explorer/commit/f5c577c86137dbb17fbce062f30a78e65d223682))

### Fix

* fix(nrtk_transforms): avoid runtime error from type hints ([`309b817`](https://github.com/Kitware/nrtk-explorer/commit/309b817344176539f6b0196dc798cda9880cfefc))

### Unknown

* Merge main to release ([`fd39df2`](https://github.com/Kitware/nrtk-explorer/commit/fd39df2f70128710779cbce356264a1fb4f252a1))

* lint ([`bd67b41`](https://github.com/Kitware/nrtk-explorer/commit/bd67b41818fe182cb5c7a279e2a1f1a0e7b59888))

* Fix type checks when missing libraries ([`8ea727a`](https://github.com/Kitware/nrtk-explorer/commit/8ea727af02539ace6054e8d74b7d907ca9f96ed8))

* Auto-merge release back to main ([`fc4fd3b`](https://github.com/Kitware/nrtk-explorer/commit/fc4fd3b16c0d91e4a29b6762b0fe7c0174df6e10))


## v0.3.0 (2024-08-07)

### Chore

* chore(deps): bump scikit-learn from 1.5.0 to 1.5.1

Bumps [scikit-learn](https://github.com/scikit-learn/scikit-learn) from 1.5.0 to 1.5.1.
- [Release notes](https://github.com/scikit-learn/scikit-learn/releases)
- [Commits](https://github.com/scikit-learn/scikit-learn/compare/1.5.0...1.5.1)

---
updated-dependencies:
- dependency-name: scikit-learn
  dependency-type: direct:production
  update-type: version-update:semver-patch
...

Signed-off-by: dependabot[bot] &lt;support@github.com&gt; ([`95001d5`](https://github.com/Kitware/nrtk-explorer/commit/95001d5d62e7988369aec2df952b336e811f8d11))

* chore(coco_utils): avoid circular import for tests ([`551fe22`](https://github.com/Kitware/nrtk-explorer/commit/551fe22faff31c35bee44c3c70cfbc6194335e78))

* chore: update npm packages ([`b8b245f`](https://github.com/Kitware/nrtk-explorer/commit/b8b245f3e801e3793051a1611050bcf15686302c))

* chore(deps-dev): bump vite from 4.5.2 to 4.5.3 in /vue-components

Bumps [vite](https://github.com/vitejs/vite/tree/HEAD/packages/vite) from 4.5.2 to 4.5.3.
- [Release notes](https://github.com/vitejs/vite/releases)
- [Changelog](https://github.com/vitejs/vite/blob/v4.5.3/packages/vite/CHANGELOG.md)
- [Commits](https://github.com/vitejs/vite/commits/v4.5.3/packages/vite)

---
updated-dependencies:
- dependency-name: vite
  dependency-type: direct:development
...

Signed-off-by: dependabot[bot] &lt;support@github.com&gt; ([`e57e3b7`](https://github.com/Kitware/nrtk-explorer/commit/e57e3b792c228cc9910eef6822583987aab50e40))

* chore(deps): bump scikit-learn from 1.4.2 to 1.5.0

Bumps [scikit-learn](https://github.com/scikit-learn/scikit-learn) from 1.4.2 to 1.5.0.
- [Release notes](https://github.com/scikit-learn/scikit-learn/releases)
- [Commits](https://github.com/scikit-learn/scikit-learn/compare/1.4.2...1.5.0)

---
updated-dependencies:
- dependency-name: scikit-learn
  dependency-type: direct:production
  update-type: version-update:semver-minor
...

Signed-off-by: dependabot[bot] &lt;support@github.com&gt; ([`3099684`](https://github.com/Kitware/nrtk-explorer/commit/30996849aae7f75a3389173da6c2f65c18f18b4c))

### Ci

* ci: trigger release ([`f0c9a84`](https://github.com/Kitware/nrtk-explorer/commit/f0c9a84038e9c323b56f4f830f43df32188cebb9))

* ci: add nightly build ([`5b50e68`](https://github.com/Kitware/nrtk-explorer/commit/5b50e68b0426ebf9bbdfda03e2b89014ce8f9cde))

### Feature

* feat(image_list): add visible columns control ([`1c87a6e`](https://github.com/Kitware/nrtk-explorer/commit/1c87a6ee89cd5e489a71bb7eaae4af8511cc9dad))

* feat(transforms): async display of ground truth annotations ([`6b434ee`](https://github.com/Kitware/nrtk-explorer/commit/6b434ee93ad04702eb21ffb05ef60b3838bf6852))

* feat: use kwcoco for coco datasets ([`782d6a3`](https://github.com/Kitware/nrtk-explorer/commit/782d6a37ce9ad2bd7f789bc6be7fc74ed8276ed5))

* feat(dataset): add force_reload parameter ([`cfb2b63`](https://github.com/Kitware/nrtk-explorer/commit/cfb2b633989e6aa192110f7889e6fa52ba8e196a))

* feat(transforms): always show ground truth

Always compute score against ground truth. ([`5c6cde6`](https://github.com/Kitware/nrtk-explorer/commit/5c6cde630b2e27050b17994041e86a40642eadde))

* feat(image_list): replace grid switch with toggle button ([`b95031d`](https://github.com/Kitware/nrtk-explorer/commit/b95031dd6ebefc3d474fd0e0f619e2ef39fa2c64))

* feat(ImageDetection): only show annotation ID for ground truth

Was showing repetitive category ID for object detection model
annotations. ([`396e3e4`](https://github.com/Kitware/nrtk-explorer/commit/396e3e4ed059c190ec72be96523d7c2f6a3ba77b))

* feat: toggle ground truth/predictions annotations

- Toggle ground truth/predictions annotations for source and
  transformation images.
- Compute COCO score (NRTK) instead of embeddings cartesian distance.
- Add unit tests for the coco_utils.py newly module. ([`0ab0b5b`](https://github.com/Kitware/nrtk-explorer/commit/0ab0b5bdbf5e09031df24eebbdfad273ece50a4a))

* feat(image_list): add search and fullscreen controls ([`3196272`](https://github.com/Kitware/nrtk-explorer/commit/31962720375cf65ab8c2506e1527afa5c7f23c4d))

* feat(ImageDetection): keep tooltip visible and hide scrollbars

* fix img css position to block to avoid following image
content from shifting as image did not contribute to component width.
* refactor canvas context creation. ([`d235d14`](https://github.com/Kitware/nrtk-explorer/commit/d235d14bd03f596a36d85303cf22a2e4dca73526))

* feat(image_list): add embeddings distance to image table ([`1d4f6dd`](https://github.com/Kitware/nrtk-explorer/commit/1d4f6ddcc35b7fd74fde0728d9eff712c7572fdf))

* feat(image_list): add table panel under tab ([`172b256`](https://github.com/Kitware/nrtk-explorer/commit/172b2563ca9a0b16ad8dd1b692f72431b2c8500a))

* feat(image_list): spinner for loading images ([`1c162e0`](https://github.com/Kitware/nrtk-explorer/commit/1c162e0f016ceee5210de683198ba72ec00a1119))

* feat(image_list): group original and transformed images ([`6f0d803`](https://github.com/Kitware/nrtk-explorer/commit/6f0d803c0e8884efd6337f6328659d3388442709))

### Fix

* fix(core): filter image selection by ground truth categories

Closes #74 ([`d0ccc0a`](https://github.com/Kitware/nrtk-explorer/commit/d0ccc0a0fc4b9cf642e4dec25f6e86948806f068))

* fix(embeddings): hover on original image highlights ([`0b7d00b`](https://github.com/Kitware/nrtk-explorer/commit/0b7d00bf0adac1d9ac89023c58dc90ef8c721877))

* fix(dataset): prefer implicit return types

get_dataset() returns a CocoDataset, not a Dataset. ([`bc5b0ca`](https://github.com/Kitware/nrtk-explorer/commit/bc5b0ca3c73a6121f144a62e6cbc34ecc6e72089))

* fix: entry name of transforms subapp ([`363716d`](https://github.com/Kitware/nrtk-explorer/commit/363716de5fd8c0e5df2b30afcbec6d1dbf4e3979))

* fix(ImageDetection): keep the same color for same labels ([`9e0a733`](https://github.com/Kitware/nrtk-explorer/commit/9e0a7331f6fa2e60aa42c15b70634c6bc8a372c0))

* fix: dataset.py snake case and remove unused imports ([`53b6005`](https://github.com/Kitware/nrtk-explorer/commit/53b60050327e2592d5a7b973f3b1a3f65a1ea5ad))

* fix: show object detection label if no category in dataset ([`b4f9b41`](https://github.com/Kitware/nrtk-explorer/commit/b4f9b41b19eaff50924dcd52fecb726a54885d5c))

* fix(transforms): compute score for truth to transform correctly ([`141bea6`](https://github.com/Kitware/nrtk-explorer/commit/141bea6404a943a6104b66f0418ab6662935793b))

* fix: score 0 when no predictions, dataset switching bug ([`9cb8ab1`](https://github.com/Kitware/nrtk-explorer/commit/9cb8ab13d103372e2c8b541d954d5ea4ed9eebe0))

* fix(ImageDetection): keep tooltip from clipping under table

Shifting tooltip if out of window was not enough
when table size was small, and tooltip would clip
under the table footer. ([`a670d92`](https://github.com/Kitware/nrtk-explorer/commit/a670d92bc18e15d4d02100ee7f436375dff3be47))

* fix(transforms): resize transformed image for scoring

Annotation similarity scoring requires the transformed image
to be the same size as the original image. ([`86c0e2e`](https://github.com/Kitware/nrtk-explorer/commit/86c0e2e443e38bf8556a15a97d9e18599819f281))

* fix(transforms): use class agnostic scorer

Avoids error when Object Detection Model outputs
category that is not in COCO JSON. ([`d3bccfe`](https://github.com/Kitware/nrtk-explorer/commit/d3bccfec2bfb3727de551747b8552a94da38ba4d))

* fix(image_meta): add distance to meta type dict ([`43a704e`](https://github.com/Kitware/nrtk-explorer/commit/43a704e09bd121087a5bbf7cbea46263594308f9))

* fix(pyproject): set min versions for nrtk and timm ([`01ce0bb`](https://github.com/Kitware/nrtk-explorer/commit/01ce0bb78ab6e9cd5a02a0af5cc9ce59bed150e2))

* fix(ScatterPlot): after selection, start navigation mode again ([`eb65f38`](https://github.com/Kitware/nrtk-explorer/commit/eb65f3868f631340b85f1a86f325982689c97479))

* fix(embeddings): allow selection of transformed point ([`dd1650f`](https://github.com/Kitware/nrtk-explorer/commit/dd1650f6560c72ed7c7fe4cf5104a6489e5ea95a))

* fix(ImageDetection): avoid extra bottom padding on hover border ([`95235a5`](https://github.com/Kitware/nrtk-explorer/commit/95235a510c6d12ded494cf08b8da2654925e64e9))

* fix(ImageDetection): miss aligned annotations for transformed images

When transformed image resolution was different from the original image,
the annotations were not aligned with the image.

closes #60 ([`a38e30f`](https://github.com/Kitware/nrtk-explorer/commit/a38e30f821525e192e1f18a37127fec701877d9e))

* fix(embeddings): distinguish image kind on hover ([`26a670d`](https://github.com/Kitware/nrtk-explorer/commit/26a670d8f8ba8c99c486c79a822f981453a6d338))

* fix(image-list): show hover box on original or transformed ([`e61e66c`](https://github.com/Kitware/nrtk-explorer/commit/e61e66c92b6b0bdd9d9de847fcc7a6e48d439455))

### Performance

* perf(transforms): only create transformed images if visible ([`e11b422`](https://github.com/Kitware/nrtk-explorer/commit/e11b422247ba872aafacfdfc6cb29f625ceaf5a0))

### Refactor

* refactor(trame_utils): simplify and doc change_checker ([`0ac0975`](https://github.com/Kitware/nrtk-explorer/commit/0ac0975ad104fb097be6f8b48852defc087d6ab3))

* refactor(image-list): add image server

Keeps original image off state

Remove commented code ([`16a953d`](https://github.com/Kitware/nrtk-explorer/commit/16a953d7947cf6b45dc7c8a9811fab28b67433f1))

* refactor(transforms): dont duplicate annotations on context

Stashing them on state once is enough ([`65e5c8f`](https://github.com/Kitware/nrtk-explorer/commit/65e5c8f4a9ff23248d737d45f752e84f771eacf3))

* refactor(transforms): put state.loading_images in _update_images ([`2f3e244`](https://github.com/Kitware/nrtk-explorer/commit/2f3e2443091efc7b2ea8a69e77e9ea28b8c6549d))

* refactor(object_detector): add return type annotation ([`2237edf`](https://github.com/Kitware/nrtk-explorer/commit/2237edfbd04762be70ce96c1a94dbc1c768bb174))

* refactor(image_ids): remove domain types ([`834a664`](https://github.com/Kitware/nrtk-explorer/commit/834a66456cd504e5dd0766aff7f93afa1f66b69e))

* refactor(object_detector): eval returns image_id keyed dict ([`041a6eb`](https://github.com/Kitware/nrtk-explorer/commit/041a6ebfb81897133b64dc0b54fd4300556bde5c))

* refactor: fix typing on object_detector, nrtk_transforms

and trame_utils ([`ffe0349`](https://github.com/Kitware/nrtk-explorer/commit/ffe03495a89717fd77e0f278100a56e8d3ff00b5))

* refactor(transforms): remove pointless state.image_kinds ([`2308d64`](https://github.com/Kitware/nrtk-explorer/commit/2308d64f548c36cce629e60e0b0e9e215bd0a886))

* refactor: add image_ids and trame_utils modules ([`07b254c`](https://github.com/Kitware/nrtk-explorer/commit/07b254c70f7680fc48cbc5c4ae4437d23562ab20))

* refactor(image_list): use Quasar table grid mode

instead of custom grid view. ([`3fd7629`](https://github.com/Kitware/nrtk-explorer/commit/3fd7629ff3374d231e0cc87748a30e925a96de2e))

* refactor(transforms): index image meta by dataset ID ([`05fd731`](https://github.com/Kitware/nrtk-explorer/commit/05fd7313df74800b713897436119783a05b860c3))

* refactor(embeddings): don&#39;t short circuit if id is empty string ([`6696afe`](https://github.com/Kitware/nrtk-explorer/commit/6696afed0f7a519fc31dc1caff40cdba8c1487fb))

* refactor(transforms): wrap sync _update_images in async _set_source_images ([`a7128d3`](https://github.com/Kitware/nrtk-explorer/commit/a7128d33149a20ffca0d9286c304348b70184347))

* refactor(transforms): rename image_kinds.image_id_key to image_ids_list ([`20af742`](https://github.com/Kitware/nrtk-explorer/commit/20af742d1b896eeff09b0b461bc3259251709615))

* refactor(image_list): use Getter for image_id ([`6460f64`](https://github.com/Kitware/nrtk-explorer/commit/6460f641289cea7d05c33cb217a14c65111e47c0))

### Unknown

* Merge main to release ([`d67665e`](https://github.com/Kitware/nrtk-explorer/commit/d67665e98145de10a2a4281ad02c105ffd7a065d))

* embeddings,object_detector: add OOM recover fix ([`7cfba68`](https://github.com/Kitware/nrtk-explorer/commit/7cfba68cdb6c0a320ed871d85a74551b101c3ad0))

* Auto-merge release back to main ([`983afc9`](https://github.com/Kitware/nrtk-explorer/commit/983afc9dcd3250043f7a41b165a31c636d20a569))


## v0.2.2 (2024-05-22)

### Chore

* chore: remove unused python module ([`5a9271c`](https://github.com/Kitware/nrtk-explorer/commit/5a9271caeb5a9924cc272780fa3ecb143a26a523))

### Fix

* fix: remove unused libraries and python modules ([`f82b46c`](https://github.com/Kitware/nrtk-explorer/commit/f82b46c2bf7e93e0b11c24bee06c4a415497964b))

### Unknown

* Merge main to release ([`7b2e41e`](https://github.com/Kitware/nrtk-explorer/commit/7b2e41ebc0f282e0f8630052156b0d6e3db036d1))

* Auto-merge release back to main ([`cbb920a`](https://github.com/Kitware/nrtk-explorer/commit/cbb920a5d164f45667556c2fbee935dc917ef457))


## v0.2.1 (2024-05-21)

### Ci

* ci: create_release only in release branch ([`d07bdf4`](https://github.com/Kitware/nrtk-explorer/commit/d07bdf4ad712a8a2936782b1fab8a934858cedd3))

### Fix

* fix: gracefully disable nrtk transform if we have import error ([`05efbcc`](https://github.com/Kitware/nrtk-explorer/commit/05efbccf345d43b02aa86bb6ba978a77a1f65135))

### Unknown

* Update create_release.yaml ([`73f6e97`](https://github.com/Kitware/nrtk-explorer/commit/73f6e9784552588e7e36919bfda72f77df10b324))

* Merge main to release ([`511736c`](https://github.com/Kitware/nrtk-explorer/commit/511736c5cdaea66704001f3a327b744fe844adeb))

* Auto-merge release back to main ([`facc6aa`](https://github.com/Kitware/nrtk-explorer/commit/facc6aafee5b1ff17e178ea7151fb46fec407056))


## v0.2.0 (2024-05-16)

### Ci

* ci: fixture in semantic release script ([`5ce57e5`](https://github.com/Kitware/nrtk-explorer/commit/5ce57e57b18eb0c77677dc61694d6a3f52588c9e))

### Feature

* feat: support hot-reload for ui

If starting app with `nrtk_explorer --hot-reload`,
then a button appears in the upper right to reload
the ui modules and re-run Engine.ui method. ([`42ae90d`](https://github.com/Kitware/nrtk-explorer/commit/42ae90d33325b2251a8d7585776ee6ebc129c6db))

### Fix

* fix(nrtk_transforms): support new nrtk PybsmPerturber api

(cherry picked from commit efaf36a602b3383ab7a7374ec698b49a6e80d5b9) ([`edea3f8`](https://github.com/Kitware/nrtk-explorer/commit/edea3f83206799c2db8536c8a4038bcc89234ca3))

* fix: change object_detector output

(cherry picked from commit 633e5f46b22eaf594f3eab657b124f75386fff45) ([`fec5df0`](https://github.com/Kitware/nrtk-explorer/commit/fec5df0712d4743498d1f62fd56f46d94feaa22f))

* fix(ImageDetection): fallback to Unknown name when uncatagorized

Horse drawn trolly thing has category ID of 0.

(cherry picked from commit f12cd7b2432b2b7fa957602e8dc34196bb183643) ([`75a236f`](https://github.com/Kitware/nrtk-explorer/commit/75a236f5b8309e1ab0839c50ba89eead09a5a6a7))

* fix(object_detector): maintain input paths order of output predictions

Caused annotations to be overlaid on the wrong
images in image list view.

(cherry picked from commit fcc8f0a278acf9cd8837185b8f046c75c315246a) ([`1b2fdb3`](https://github.com/Kitware/nrtk-explorer/commit/1b2fdb3615063be6e92a548ec0a6ab27751a001d))

* fix(benchmarks): allow using a external COCO ds

(cherry picked from commit 34b2fdbeff7b724c542ac053d4d19fca6114939c) ([`3e7e56e`](https://github.com/Kitware/nrtk-explorer/commit/3e7e56ed3f53e0baf2649336844e669f4213bcf8))

* fix(nrtk-explorer): multi platform paths

(cherry picked from commit 0131172a2480a3e75bdb353741561e31d1625bcd) ([`cc631d7`](https://github.com/Kitware/nrtk-explorer/commit/cc631d718476286a19222debc0382295e54885a2))

* fix(nrtk_transforms): support new nrtk PybsmPerturber api ([`efaf36a`](https://github.com/Kitware/nrtk-explorer/commit/efaf36a602b3383ab7a7374ec698b49a6e80d5b9))

* fix: change object_detector output ([`633e5f4`](https://github.com/Kitware/nrtk-explorer/commit/633e5f46b22eaf594f3eab657b124f75386fff45))

* fix(ImageDetection): fallback to Unknown name when uncatagorized

Horse drawn trolly thing has category ID of 0. ([`f12cd7b`](https://github.com/Kitware/nrtk-explorer/commit/f12cd7b2432b2b7fa957602e8dc34196bb183643))

* fix(object_detector): maintain input paths order of output predictions

Caused annotations to be overlaid on the wrong
images in image list view. ([`fcc8f0a`](https://github.com/Kitware/nrtk-explorer/commit/fcc8f0a278acf9cd8837185b8f046c75c315246a))

* fix(benchmarks): allow using a external COCO ds ([`34b2fdb`](https://github.com/Kitware/nrtk-explorer/commit/34b2fdbeff7b724c542ac053d4d19fca6114939c))

* fix(nrtk-explorer): multi platform paths ([`0131172`](https://github.com/Kitware/nrtk-explorer/commit/0131172a2480a3e75bdb353741561e31d1625bcd))

### Refactor

* refactor(layout): factor out sections to functions ([`dfa9a85`](https://github.com/Kitware/nrtk-explorer/commit/dfa9a857675766fae6fdb66d3b4d68346607dea9))

### Unknown

* Merge main to release ([`e32828d`](https://github.com/Kitware/nrtk-explorer/commit/e32828d8011151e63093864411b037488275fa21))

* Bump ubelt from 1.3.4 to 1.3.5

Bumps [ubelt](https://github.com/Erotemic/ubelt) from 1.3.4 to 1.3.5.
- [Release notes](https://github.com/Erotemic/ubelt/releases)
- [Changelog](https://github.com/Erotemic/ubelt/blob/main/CHANGELOG.md)
- [Commits](https://github.com/Erotemic/ubelt/compare/v1.3.4...v1.3.5)

---
updated-dependencies:
- dependency-name: ubelt
  dependency-type: direct:production
  update-type: version-update:semver-patch
...

Signed-off-by: dependabot[bot] &lt;support@github.com&gt; ([`87a292d`](https://github.com/Kitware/nrtk-explorer/commit/87a292df21262e9f1f723a5a9be82d3fa3f89acc))

* Bump scikit-learn from 1.4.1.post1 to 1.4.2

Bumps [scikit-learn](https://github.com/scikit-learn/scikit-learn) from 1.4.1.post1 to 1.4.2.
- [Release notes](https://github.com/scikit-learn/scikit-learn/releases)
- [Commits](https://github.com/scikit-learn/scikit-learn/compare/1.4.1.post1...1.4.2)

---
updated-dependencies:
- dependency-name: scikit-learn
  dependency-type: direct:production
  update-type: version-update:semver-patch
...

Signed-off-by: dependabot[bot] &lt;support@github.com&gt; ([`a8a4862`](https://github.com/Kitware/nrtk-explorer/commit/a8a4862075cc57dc891ef40e6d46f9fbac29a267))

* Auto-merge release back to main ([`12ea17d`](https://github.com/Kitware/nrtk-explorer/commit/12ea17d04d5790f9b5abea53684b34d2faab8b46))


## v0.1.2 (2024-04-19)

### Fix

* fix(nrtk-explorer): fix readme ([`968e42e`](https://github.com/Kitware/nrtk-explorer/commit/968e42e38d0b9a15d62b4a27681aa1df300abde4))

* fix(workflow): do not install uneeded deps ([`a29260f`](https://github.com/Kitware/nrtk-explorer/commit/a29260f2abcbc81d19c607d1f8c143bd435d4073))

### Unknown

* Merge main to release ([`40e7ad5`](https://github.com/Kitware/nrtk-explorer/commit/40e7ad58264254bec2c5b0014aff68a3d82f3e2e))

* Auto-merge release back to main ([`0981c3c`](https://github.com/Kitware/nrtk-explorer/commit/0981c3caaa4a120f24a3b345a487e73df510d0e7))


## v0.1.1 (2024-04-19)

### Fix

* fix(core): removed unused default dataset ([`5f870ef`](https://github.com/Kitware/nrtk-explorer/commit/5f870ef74d8445d786990641fdad12b8afa065f2))

* fix(sample): sample dataset categories ([`e85de50`](https://github.com/Kitware/nrtk-explorer/commit/e85de50d59c26f97ddccf23c3d893353855a60d4))

### Unknown

* fix(workflow) workflow fixes ([`e7540f1`](https://github.com/Kitware/nrtk-explorer/commit/e7540f12e0f19e529b685160fc28d82a1567e8a6))

* Auto-merge release back to main ([`f652c12`](https://github.com/Kitware/nrtk-explorer/commit/f652c1294fffc930fd6d06daa87d55386f812b0f))


## v0.1.0 (2024-04-19)

### Documentation

* docs(readme): add usage section ([`7bfdbc4`](https://github.com/Kitware/nrtk-explorer/commit/7bfdbc4ad511eadda75c14aca3d310b2cd9a996a))

* docs(readme): add usage example ([`b668617`](https://github.com/Kitware/nrtk-explorer/commit/b6686178eae2ea22be410260e4a3d1f1eb182403))

### Feature

* feat(web): add test apps ([`f58c6ea`](https://github.com/Kitware/nrtk-explorer/commit/f58c6eaf8b2cc27ea331afaa91423f81deeb551b))

### Fix

* fix(cli): update executable name to use - ([`cab041b`](https://github.com/Kitware/nrtk-explorer/commit/cab041b4ca675b0eaca9d6c02c93615a4f1806a8))

* fix(dataset): better handling of dataset arg ([`b8bb107`](https://github.com/Kitware/nrtk-explorer/commit/b8bb1075b1a206118ce3c0d18ae726ee1f447dc8))

### Unknown

* Merge main to release ([`6e871d2`](https://github.com/Kitware/nrtk-explorer/commit/6e871d26b2039197bcc6b6e9c14c6e1495d6b9b0))

* Auto-merge release back to main ([`2c3cd2b`](https://github.com/Kitware/nrtk-explorer/commit/2c3cd2b36508a43fccb595995ba5cc7a2ea9f7b1))


## v0.0.6 (2024-04-19)

### Fix

* fix(nrtk-explorer): fix tests ([`2693689`](https://github.com/Kitware/nrtk-explorer/commit/269368975e16e21d9caf2575ebeba717c7ff7543))

### Unknown

* Merge main to release ([`3de4c18`](https://github.com/Kitware/nrtk-explorer/commit/3de4c18ae7b4d87b7b74dd5bc62e121e01238ebe))

* Auto-merge release back to main ([`e26a9c4`](https://github.com/Kitware/nrtk-explorer/commit/e26a9c41b47c95d9cf4864356d1fb66d15ab279b))


## v0.0.5 (2024-04-19)

### Fix

* fix(nrtk-explorer): fix tag ([`c366639`](https://github.com/Kitware/nrtk-explorer/commit/c366639eff412acddf5032f1d1e7f7aaee45b557))

* fix(nrtk-explorer): fix readme ([`3fa6717`](https://github.com/Kitware/nrtk-explorer/commit/3fa6717604bd071d1bf1298400e76fd9353859cc))

* fix(nrtk-explorer): fix image in readme ([`f3964d4`](https://github.com/Kitware/nrtk-explorer/commit/f3964d404c1a296f8bc2394be2ffdbd8ff476714))

### Unknown

* Merge main to release ([`49ccd85`](https://github.com/Kitware/nrtk-explorer/commit/49ccd85f7dbd51aed7feaba5eb5b0b67c982b5ed))

* Auto-merge release back to main ([`4cfb5d5`](https://github.com/Kitware/nrtk-explorer/commit/4cfb5d5cc8a2f320cd2b806353969fcdc80b49a0))

* Merge main to release ([`c5ea4c4`](https://github.com/Kitware/nrtk-explorer/commit/c5ea4c4af7172ff8b3928aead1026d2fef25d3bc))

* Auto-merge release back to main ([`0cd0732`](https://github.com/Kitware/nrtk-explorer/commit/0cd07325b62152da316448be466e2eb350ed3f63))


## v0.0.4 (2024-04-19)

### Fix

* fix(nrtk-explorer): fix image in readme ([`80850aa`](https://github.com/Kitware/nrtk-explorer/commit/80850aa0ad37343ca6b0a2c0961c54d92ba23a81))


## v0.0.3 (2024-04-18)

### Fix

* fix(nrtk-explorer): removed large tests datasets ([`b219a75`](https://github.com/Kitware/nrtk-explorer/commit/b219a75402fcbd534e881fa66732a204817a534a))


## v0.0.2 (2024-04-18)

### Fix

* fix(nrtk-explorer): new release ([`51c0607`](https://github.com/Kitware/nrtk-explorer/commit/51c06075c83d93bf61db772cdbe4470b477864f5))


## v0.0.1 (2024-04-18)

### Ci

* ci(workflow): add a new version ([`9367fc4`](https://github.com/Kitware/nrtk-explorer/commit/9367fc4d49466adbe5110b36153f4d06720a154b))

* ci(workflow): remove pre-commit ([`b753c15`](https://github.com/Kitware/nrtk-explorer/commit/b753c15a395fa818ad9f5c1f04583df5fb9bbafa))

* ci(workflow): add semantic-release task ([`2f3a00c`](https://github.com/Kitware/nrtk-explorer/commit/2f3a00ce7cbc3364b26e90c8ace1174b0284ff48))

* ci: add flake8 tests (#3) ([`7dcd11f`](https://github.com/Kitware/nrtk-explorer/commit/7dcd11fb367d7112d53510cc9a422ce258255095))

* ci: add unit tests (#2) ([`09b4b1d`](https://github.com/Kitware/nrtk-explorer/commit/09b4b1dbc7fcaf03aaa1bad6b7ce0030feee6389))

### Documentation

* docs(readme): improve readme ([`c2c6224`](https://github.com/Kitware/nrtk-explorer/commit/c2c622411c7b432e6c4327b9531843c419f35a5e))

### Fix

* fix(nrtk-explorer): new release ([`de216a8`](https://github.com/Kitware/nrtk-explorer/commit/de216a81863d134735415fa9639abb05ca2b111c))

### Unknown

* Auto-merge release back to main ([`d3df0ec`](https://github.com/Kitware/nrtk-explorer/commit/d3df0ecf748664d806f09ad11e2bbd71a0bca1dd))

* add obj detect model ui (#49)

* Added COCO Object detection 2017 dataset

* add obj detect model ui

* update github actions actions ([`774624e`](https://github.com/Kitware/nrtk-explorer/commit/774624ea9eb8046c27cea6e11854dd1539c1075a))

* Ignore unrecognized cli arguments instead of crashing ([`59c3af8`](https://github.com/Kitware/nrtk-explorer/commit/59c3af8baca67751c62bf5cc168474521a603d4c))

* Automatically build frontend on pip install ([`02bf529`](https://github.com/Kitware/nrtk-explorer/commit/02bf5296269280cff1be05001d2b3ab9f7da4cd8))

* Place code under src dir and use hatchling for building ([`7bb539e`](https://github.com/Kitware/nrtk-explorer/commit/7bb539e5635ba52913a76a26bdb2704c7c04b643))

* Allow user to resize the UI panels ([`e4d517c`](https://github.com/Kitware/nrtk-explorer/commit/e4d517ce7f481ea20903639af0482ee67dc057b1))

* Improve the appearance of the settings panel ([`1966d00`](https://github.com/Kitware/nrtk-explorer/commit/1966d0085b80c10359f2604ac461a2f1b584aa46))

* Rework point highlighting to consider src and trans ([`abf9464`](https://github.com/Kitware/nrtk-explorer/commit/abf94642079c8572ec3585e537deb8bb370724ff))

* Handle different image sizes and aspects ([`33b89bc`](https://github.com/Kitware/nrtk-explorer/commit/33b89bc94f7d041ad100d3076ce75ecfa2605b04))

* Support datasets that uses ids diff to offsets ([`971c497`](https://github.com/Kitware/nrtk-explorer/commit/971c497c7792410368bee6e2b470cf06e8742070))

* Fix reactivity in imagedetection thumbnails ([`598a452`](https://github.com/Kitware/nrtk-explorer/commit/598a4529a4fea877fa5c016f6bd25f9763fa30e7))

* Select images by filtering based on annotation categories ([`3a0cd8f`](https://github.com/Kitware/nrtk-explorer/commit/3a0cd8f224031c0ad94677ee6b9f7b0361a177e3))

* toggle hide source points in scatterplot ([`34fcf17`](https://github.com/Kitware/nrtk-explorer/commit/34fcf174dd2b93443987392ce4245fe230cb8e18))

* imagedetection: remove ref properties ([`405428a`](https://github.com/Kitware/nrtk-explorer/commit/405428ab5a732eeb5afab7bdd84e054f676b1758))

* enable hovering highlight in all components (#36) ([`3044bc5`](https://github.com/Kitware/nrtk-explorer/commit/3044bc51dbacc360885ed2da93446092dbea585f))

* mypy: Fix library code so it passes mypy ([`3cf55ef`](https://github.com/Kitware/nrtk-explorer/commit/3cf55efabb9a0e64292d349c30cee120dbba9108))

* mypy: Add python typing CI ([`63a1f7e`](https://github.com/Kitware/nrtk-explorer/commit/63a1f7e91cf1fd88acbfe24694a407dad132c542))

* add cli flag for passing paths of datasets (#35)

* add cli flag for passing paths of datasets

* scatterplot: fix point highlight ([`35f55c5`](https://github.com/Kitware/nrtk-explorer/commit/35f55c51166c178de0b1f22b912ded8c6e9bbc32))

* add batching and make it a param (#31)

* add batching and make it a param

* Fixed benchmark for embeddings_extractor ([`65c0d57`](https://github.com/Kitware/nrtk-explorer/commit/65c0d573147888ce0ffb95bc1e7ff076c720ceb5))

* update npm pkgs (#33)

* update npm pkgs

* scatterplot: fixed error with sequences ([`29b041e`](https://github.com/Kitware/nrtk-explorer/commit/29b041e4b5582bf1a683d2eb590658be9ea143ad))

* Bump scikit-learn from 1.4.0 to 1.4.1.post1 (#32)

Bumps [scikit-learn](https://github.com/scikit-learn/scikit-learn) from 1.4.0 to 1.4.1.post1.
- [Release notes](https://github.com/scikit-learn/scikit-learn/releases)
- [Commits](https://github.com/scikit-learn/scikit-learn/compare/1.4.0...1.4.1.post1)

---
updated-dependencies:
- dependency-name: scikit-learn
  dependency-type: direct:production
  update-type: version-update:semver-patch
...

Signed-off-by: dependabot[bot] &lt;support@github.com&gt;
Co-authored-by: dependabot[bot] &lt;49699333+dependabot[bot]@users.noreply.github.com&gt; ([`0de4d01`](https://github.com/Kitware/nrtk-explorer/commit/0de4d01fe1a803c0329636ea263a0e5023e991c8))

* umap: add params (#30)

- fixes to the ReduceManager
- Refactor to the ScatterPlot ([`541d413`](https://github.com/Kitware/nrtk-explorer/commit/541d4132314a0c48f8ebeeda868553f23a9adb7c))

* Combine original and transformed scatter plots into a single plot (#29) ([`4913c95`](https://github.com/Kitware/nrtk-explorer/commit/4913c95ffddd65f7e7baccedbbe3d44fa099d6eb))

* embeddigns: add loading behavior while computing (#28) ([`9b667fe`](https://github.com/Kitware/nrtk-explorer/commit/9b667fe13ca8536fa95940172447447783b93be0))

* Add a couple of transforms that use nrtk&#39;s perturbers (#27) ([`cd02396`](https://github.com/Kitware/nrtk-explorer/commit/cd0239626b8e567a64e5bc5d1afe621631133eb6))

* fixes in the reactivity of scatterplot (#22) ([`3af59a4`](https://github.com/Kitware/nrtk-explorer/commit/3af59a4ab0dc6ce6117a2eb76d67afac67b2db24))

* Bump vite from 4.4.12 to 4.5.2 in /vue-components (#26)

Bumps [vite](https://github.com/vitejs/vite/tree/HEAD/packages/vite) from 4.4.12 to 4.5.2.
- [Release notes](https://github.com/vitejs/vite/releases)
- [Changelog](https://github.com/vitejs/vite/blob/v4.5.2/packages/vite/CHANGELOG.md)
- [Commits](https://github.com/vitejs/vite/commits/v4.5.2/packages/vite)

---
updated-dependencies:
- dependency-name: vite
  dependency-type: direct:development
...

Signed-off-by: dependabot[bot] &lt;support@github.com&gt;
Co-authored-by: dependabot[bot] &lt;49699333+dependabot[bot]@users.noreply.github.com&gt; ([`3882dc5`](https://github.com/Kitware/nrtk-explorer/commit/3882dc5efe50e8848f2cb34d6dff2ea3fc53bba6))

* Add vue CI (#23) ([`1594b36`](https://github.com/Kitware/nrtk-explorer/commit/1594b36219454c25aaa8576cce7d1ad86e0dcb03))

* Enable CUDA backend (#24)

* Enable CUDA backend

* Update pyproject.toml ([`dce73d8`](https://github.com/Kitware/nrtk-explorer/commit/dce73d8d3010e02b74abaec4ca6a39bb858b635f))

* cosmetic fixes in embeddings and core parameters UI (#25) ([`74278b8`](https://github.com/Kitware/nrtk-explorer/commit/74278b8d2e122a4ce08ee099fdd5d5c7dd9be1fe))

* Bump scikit-learn from 1.3.2 to 1.4.0 (#20)

Bumps [scikit-learn](https://github.com/scikit-learn/scikit-learn) from 1.3.2 to 1.4.0.
- [Release notes](https://github.com/scikit-learn/scikit-learn/releases)
- [Commits](https://github.com/scikit-learn/scikit-learn/compare/1.3.2...1.4.0)

---
updated-dependencies:
- dependency-name: scikit-learn
  dependency-type: direct:production
  update-type: version-update:semver-minor
...

Signed-off-by: dependabot[bot] &lt;support@github.com&gt;
Co-authored-by: dependabot[bot] &lt;49699333+dependabot[bot]@users.noreply.github.com&gt; ([`bb15d68`](https://github.com/Kitware/nrtk-explorer/commit/bb15d68f5ad598df58912a5ae1522a3839116b72))

* Refactor image id handling. (#19)

- Moves logic to the core application (Random selection and number of images to load).
- Fixes wrong transformation when using random selection
- Connects plots and thumbnails so that hovering is reflected.
- Futher improving performance by sharing a cache of the feature
  extractions between the source and transformation dataset. ([`84482e6`](https://github.com/Kitware/nrtk-explorer/commit/84482e6f0c781345204aca38e4187ee8e1c12fdc))

* Use trame&#39;s new server.context and translator instead of our implementation (#21) ([`6a02609`](https://github.com/Kitware/nrtk-explorer/commit/6a02609e42eb08ebe9cb760d6773ac81a1b96470))

* Transforms plot shows origin and transformations (#18)

* Improve scatter plots:

- Transforms plot shows origin and trans.
- Source and Transform plots are syncronized.

* Multiple improvements:

- Embedding state is shared between transformation and origin.
- Change in camera in transformation plot reflects in source.
- Remove controls in transformation plot
- Share the same feature extractor for transformation and source
  feature extractor. ([`2d14c21`](https://github.com/Kitware/nrtk-explorer/commit/2d14c21bebaac23b7f56357bdcb666f8d6a301e9))

* Add mechanism to automatically generate transform parameters UI (#17)

* Add mechanism to automatically generate transform parameters UI

* Integrate dynamic transform parameters in the TransformsApp ([`88a140e`](https://github.com/Kitware/nrtk-explorer/commit/88a140e3149aff7ba26a99c52aa77bdf5b039fd3))

* Bump semantic-release from 19.0.2 to 19.0.3 in /vue-components (#15)

Bumps [semantic-release](https://github.com/semantic-release/semantic-release) from 19.0.2 to 19.0.3.
- [Release notes](https://github.com/semantic-release/semantic-release/releases)
- [Commits](https://github.com/semantic-release/semantic-release/compare/v19.0.2...v19.0.3)

---
updated-dependencies:
- dependency-name: semantic-release
  dependency-type: direct:development
...

Signed-off-by: dependabot[bot] &lt;support@github.com&gt;
Co-authored-by: dependabot[bot] &lt;49699333+dependabot[bot]@users.noreply.github.com&gt; ([`f13d0ee`](https://github.com/Kitware/nrtk-explorer/commit/f13d0ee82b0b2a1d0509935d9d43425f5f174a52))

* Bump postcss from 8.4.27 to 8.4.32 in /vue-components (#16)

Bumps [postcss](https://github.com/postcss/postcss) from 8.4.27 to 8.4.32.
- [Release notes](https://github.com/postcss/postcss/releases)
- [Changelog](https://github.com/postcss/postcss/blob/main/CHANGELOG.md)
- [Commits](https://github.com/postcss/postcss/compare/8.4.27...8.4.32)

---
updated-dependencies:
- dependency-name: postcss
  dependency-type: indirect
...

Signed-off-by: dependabot[bot] &lt;support@github.com&gt;
Co-authored-by: dependabot[bot] &lt;49699333+dependabot[bot]@users.noreply.github.com&gt; ([`9830256`](https://github.com/Kitware/nrtk-explorer/commit/983025629ca5d8efa1006e13337ac38bb08e81e9))

* Bump vite from 4.4.7 to 4.4.12 in /vue-components (#14)

Bumps [vite](https://github.com/vitejs/vite/tree/HEAD/packages/vite) from 4.4.7 to 4.4.12.
- [Release notes](https://github.com/vitejs/vite/releases)
- [Changelog](https://github.com/vitejs/vite/blob/v4.4.12/packages/vite/CHANGELOG.md)
- [Commits](https://github.com/vitejs/vite/commits/v4.4.12/packages/vite)

---
updated-dependencies:
- dependency-name: vite
  dependency-type: direct:development
...

Signed-off-by: dependabot[bot] &lt;support@github.com&gt;
Co-authored-by: dependabot[bot] &lt;49699333+dependabot[bot]@users.noreply.github.com&gt; ([`f1e3dfb`](https://github.com/Kitware/nrtk-explorer/commit/f1e3dfb02d4cbfbbf2993825c41e296a59838fdc))

* update name to nrtk-explorer (#13) ([`3af8f0b`](https://github.com/Kitware/nrtk-explorer/commit/3af8f0bc15ce72f50517d12998bc92c3cbbc9473))

* Create LICENSE (#12)

* Create LICENSE

* Update LICENSE ([`c5ea57a`](https://github.com/Kitware/nrtk-explorer/commit/c5ea57ade7f9e3fd9c7c5a0a6de6bdf9256f8ef6))

* Bump smqtk-detection[centernet,torch] from 0.20.0 to 0.20.1 (#10)

Bumps [smqtk-detection[centernet,torch]](https://github.com/Kitware/SMQTK-Detection) from 0.20.0 to 0.20.1.
- [Release notes](https://github.com/Kitware/SMQTK-Detection/releases)
- [Changelog](https://github.com/Kitware/SMQTK-Detection/blob/master/docs/release_notes.rst)
- [Commits](https://github.com/Kitware/SMQTK-Detection/compare/v0.20.0...v0.20.1)

---
updated-dependencies:
- dependency-name: smqtk-detection[centernet,torch]
  dependency-type: direct:production
  update-type: version-update:semver-patch
...

Signed-off-by: dependabot[bot] &lt;support@github.com&gt;
Co-authored-by: dependabot[bot] &lt;49699333+dependabot[bot]@users.noreply.github.com&gt; ([`5f5a658`](https://github.com/Kitware/nrtk-explorer/commit/5f5a6588032147a96a9e3510204b11c0242510f1))

* Bump scikit-image from 0.21.0 to 0.22.0 (#5)

Bumps [scikit-image](https://github.com/scikit-image/scikit-image) from 0.21.0 to 0.22.0.
- [Release notes](https://github.com/scikit-image/scikit-image/releases)
- [Changelog](https://github.com/scikit-image/scikit-image/blob/main/RELEASE.txt)
- [Commits](https://github.com/scikit-image/scikit-image/compare/v0.21.0...v0.22.0)

---
updated-dependencies:
- dependency-name: scikit-image
  dependency-type: direct:production
  update-type: version-update:semver-minor
...

Signed-off-by: dependabot[bot] &lt;support@github.com&gt;
Co-authored-by: dependabot[bot] &lt;49699333+dependabot[bot]@users.noreply.github.com&gt; ([`a1291e7`](https://github.com/Kitware/nrtk-explorer/commit/a1291e747acbc237dd30c5fd8c7b05df95c9398c))

* loosen pip deps (#11) ([`df54c9c`](https://github.com/Kitware/nrtk-explorer/commit/df54c9cd0f0c8b86824b8e2c90e85eb2b5864760))

* Bump ubelt from 1.3.2 to 1.3.4 (#7)

Bumps [ubelt](https://github.com/Erotemic/ubelt) from 1.3.2 to 1.3.4.
- [Release notes](https://github.com/Erotemic/ubelt/releases)
- [Changelog](https://github.com/Erotemic/ubelt/blob/main/CHANGELOG.md)
- [Commits](https://github.com/Erotemic/ubelt/compare/v1.3.2...v1.3.4)

---
updated-dependencies:
- dependency-name: ubelt
  dependency-type: direct:production
  update-type: version-update:semver-patch
...

Signed-off-by: dependabot[bot] &lt;support@github.com&gt;
Co-authored-by: dependabot[bot] &lt;49699333+dependabot[bot]@users.noreply.github.com&gt; ([`87b18a1`](https://github.com/Kitware/nrtk-explorer/commit/87b18a17339ecb6b4fb8896d2f158794aef43870))

* Bump scikit-learn from 1.3.0 to 1.3.2 (#9)

Bumps [scikit-learn](https://github.com/scikit-learn/scikit-learn) from 1.3.0 to 1.3.2.
- [Release notes](https://github.com/scikit-learn/scikit-learn/releases)
- [Commits](https://github.com/scikit-learn/scikit-learn/compare/1.3.0...1.3.2)

---
updated-dependencies:
- dependency-name: scikit-learn
  dependency-type: direct:production
  update-type: version-update:semver-patch
...

Signed-off-by: dependabot[bot] &lt;support@github.com&gt;
Co-authored-by: dependabot[bot] &lt;49699333+dependabot[bot]@users.noreply.github.com&gt; ([`f4c3dc1`](https://github.com/Kitware/nrtk-explorer/commit/f4c3dc19c3993378eb4f9a73f12d5deacd6240fa))

* Create dependabot.yml (#4) ([`0d8d663`](https://github.com/Kitware/nrtk-explorer/commit/0d8d663499c174168b8a1058588c5c2b2646aa33))

* Create black ci workflow (#1)

* Create black ci workflow

* Update black.yml ([`378c2d1`](https://github.com/Kitware/nrtk-explorer/commit/378c2d14d09c9f31ca63528a2343eccb92e5b9a9))

* Pass black tool ([`de62d13`](https://github.com/Kitware/nrtk-explorer/commit/de62d134a67baff2bd26f0944c691332208ca920))

* Merge branch &#39;rename-to-nrtk-explorer&#39; into &#39;main&#39;

Rename to nrtk explorer

See merge request alesgenova/cdao!7 ([`6aaf930`](https://github.com/Kitware/nrtk-explorer/commit/6aaf9304c1cd3e4200cc06dde4baa4f5523e99a5))

* Merge branch &#39;split-app&#39; into &#39;main&#39;

Split core app into to subapps

See merge request alesgenova/cdao!6 ([`f677afb`](https://github.com/Kitware/nrtk-explorer/commit/f677afba5a1074d4fc8735f7d2bf8eed050a048b))

* rename to nrtk-explorer ([`4f99199`](https://github.com/Kitware/nrtk-explorer/commit/4f991995be81ac91b5481cf4a5acf306f5476c6a))

* Add Embeddings plot for tranformed images ([`232abc5`](https://github.com/Kitware/nrtk-explorer/commit/232abc56e011fb3d0ad868fa44e15745865e2fcf))

* split core app into two apps ([`661801e`](https://github.com/Kitware/nrtk-explorer/commit/661801ea7494c98e29e6bf4b218b25c61f01a822))

* Merge branch &#39;add-embbedings-cache&#39; into &#39;main&#39;

Separate into subapps and benchmarks

See merge request alesgenova/cdao!5 ([`142a9cb`](https://github.com/Kitware/nrtk-explorer/commit/142a9cb79f468519a72ebf91ded3d434c8c5a1ec))

* Separate into subapps and benchmarks ([`892731b`](https://github.com/Kitware/nrtk-explorer/commit/892731be8afbfae781eabec8b5f3affbaf81b566))

* Merge branch &#39;integrate-embeddings-app&#39; into &#39;main&#39;

Integrate the embeddings app into the main app

See merge request alesgenova/cdao!4 ([`fd6c33c`](https://github.com/Kitware/nrtk-explorer/commit/fd6c33c51cec77252945c5a4fd20a72e55c3a150))

* Integrate the embeddings app into the main app ([`1668be8`](https://github.com/Kitware/nrtk-explorer/commit/1668be8eb3e48dcc22370efd3b2ff6aa9b3f62fd))

* Merge branch &#39;fix-params-embbeddings&#39; into &#39;main&#39;

embbeddings: added parameters

See merge request alesgenova/cdao!3 ([`d941fcd`](https://github.com/Kitware/nrtk-explorer/commit/d941fcdb17e29025b15e4f7cb6d435af2ca64762))

* added benchmarks tests ([`dba7e20`](https://github.com/Kitware/nrtk-explorer/commit/dba7e2075c6565ee39a756537573e20fc5f89c8f))

* Add dataset; refactor ([`25de9a4`](https://github.com/Kitware/nrtk-explorer/commit/25de9a44af0f73a1dff7f061b3cadc446514d334))

* Fix embedding visualization not appearing in the embeddings app ([`210eeef`](https://github.com/Kitware/nrtk-explorer/commit/210eeef5e64bff448ec169b8accddeb8bd6aa882))

* embbeddings: big refactor ([`f46dd2b`](https://github.com/Kitware/nrtk-explorer/commit/f46dd2ba41e3a189da975e47fd24c9caa505feb1))

* Merge branch &#39;adding-embeddings&#39; into &#39;main&#39;

First version of the embeddings app/viz

See merge request alesgenova/cdao!2 ([`228beaf`](https://github.com/Kitware/nrtk-explorer/commit/228beaf92ae958c9aba26eb54d507b6d7c28c50a))

* Add 3D visualization for the embeddings ([`1400eef`](https://github.com/Kitware/nrtk-explorer/commit/1400eef062a3f98ffba0d8a0eb1bdd38385b1d4c))

* Merge branch &#39;adding-embeddings&#39; into &#39;adding-embeddings&#39;

Adding embeddings

See merge request alesgenova/cdao!1 ([`863fb8f`](https://github.com/Kitware/nrtk-explorer/commit/863fb8fe378322e656dd130ed0674f7b5604f264))

* readyforshow ([`642899d`](https://github.com/Kitware/nrtk-explorer/commit/642899d42dc32272d18478f137525834f3eac68a))

* test ([`d65599a`](https://github.com/Kitware/nrtk-explorer/commit/d65599a096a007a98df3a9cce19f6456575161b7))

* Switch from trame-vuetify to trame-quasar ([`0110f16`](https://github.com/Kitware/nrtk-explorer/commit/0110f1608efa4c3ab54e57ccf8183f964e245220))

* Add annotation overlay when mouse hovers ([`f3a38c9`](https://github.com/Kitware/nrtk-explorer/commit/f3a38c9a7a5d5db53f0a3869114b60d579914a2c))

* Initial commit ([`881cc67`](https://github.com/Kitware/nrtk-explorer/commit/881cc679944c0382869c9a1d0e65d7f193b3af7d))
