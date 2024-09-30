<template>
    <div v-html="source" class="text-left">
    </div>
</template>

<script>

// import VueMarkdown from 'vue-markdown-render'
// import MarkdownItAnchor from 'markdown-it-anchor';

import { marked } from "marked";
import HelpText from '@/docs/help_content/help.md?raw';

export default {
  name: "HelpContent",
  data() {
    return {
    source: marked.parse(HelpText)
    }
  },
}
</script>
