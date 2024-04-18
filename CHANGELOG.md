# CHANGELOG



## v0.0.0 (2024-04-18)

### Ci

* ci(workflow): remove pre-commit ([`b9ad36c`](https://github.com/Kitware/nrtk-explorer/commit/b9ad36cfc20090f93bf258b7698060cb4759d962))

* ci(workflow): add semantic-release task ([`2f3a00c`](https://github.com/Kitware/nrtk-explorer/commit/2f3a00ce7cbc3364b26e90c8ace1174b0284ff48))

* ci: add flake8 tests (#3) ([`7dcd11f`](https://github.com/Kitware/nrtk-explorer/commit/7dcd11fb367d7112d53510cc9a422ce258255095))

* ci: add unit tests (#2) ([`09b4b1d`](https://github.com/Kitware/nrtk-explorer/commit/09b4b1dbc7fcaf03aaa1bad6b7ce0030feee6389))

### Documentation

* docs(readme): improve readme ([`c2c6224`](https://github.com/Kitware/nrtk-explorer/commit/c2c622411c7b432e6c4327b9531843c419f35a5e))

### Unknown

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