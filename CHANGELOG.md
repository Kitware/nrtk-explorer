# CHANGELOG



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
