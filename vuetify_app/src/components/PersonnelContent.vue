<template>
    <div v-html="source" class="text-left">
    </div>
</template>

<script>

// import VueMarkdown from 'vue-markdown-render'
// import MarkdownItAnchor from 'markdown-it-anchor';

import { marked } from "marked";
import Text from '@/docs/about_content/about_UI_v1.2.md?raw';

export default {
  name: "PersonnelContent",
  data() {
    return {
    source: marked.parse(Text)
    }
  },
}
</script>
