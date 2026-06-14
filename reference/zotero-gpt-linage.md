这是zotero的一个插件提供的功能，通过油猴脚本，使得zotero内的聊天框可以和gpt等网页版agent同步，我觉得这个数据获取流程对我们想实现的功能有很大价值，比起每次调用skill哪怕快照都要更好
恰好tabbit妙招功能提供脚本服务，我觉得可以做成更好的接口

```javascript
// ==UserScript==
// @name         Zotero GPT Connector
// @description  Zotero GPT Pro: Supports virtually all the AI platforms you know.
// @namespace    http://tampermonkey.net/
// @icon         https://github.com/MuiseDestiny/zotero-gpt/blob/bootstrap/addon/chrome/content/icons/favicon.png?raw=true
// @noframes
// @author       Polygon
// @version      5.4.6
// @match        https://chatgpt.com/*
// @match        https://gemini.google.com/*
// @match        https://poe.com/*
// @match        https://www.kimi.com/*
// @match        https://chatglm.cn/*
// @match        https://yiyan.baidu.com/*
// @match        https://qianwen.aliyun.com/*
// @match        https://claude.ai/*
// @match        https://mytan.maiseed.com.cn/*
// @match        https://mychandler.bet/*
// @match        https://chat.deepseek.com/*
// @match        https://www.doubao.com/chat/*
// @match        https://*.chatshare.biz/*
// @match        https://chat.kelaode.ai/*
// @match        https://chat.rawchat.cn/*
// @match        https://node.dawuai.buzz/*
// @match        https://aistudio.google.com/*
// @match        https://claude.ai0.cn/*
// @match        https://grok.com/*
// @match        https://china.aikeji.vip/*
// @match        https://chatgtp.chat/*
// @match        https://iai.aichatos8.com.cn/*
// @match        https://share.mosha.cloud/*
// @match        https://node.leadyven.com/*
// @match        https://*.bestaistore.com/*
// @match        https://www.chatgptnet.org/*
// @match        https://node3.leadyven.com/*
// @match        https://leopard-x.memofun.net/*
// @include      /.+gpt2share.+/
// @include      /.+rawchat.+/
// @include      /.+sharedchat.+/
// @include      /.+freeoai.+/
// @include      /.+sharesai.+/
// @include      /.+qwen.+/
// @include      /.+coze.+/
// @include      /.+grok.+/
// @include      /.+qianwen.+/
// @include      /.+chatopens.+/
// @include      /.+kelaode.+/
// @include      /.+askmanyai.+/
// @include      /.+4399ai.+/
// @include      /.+minimaxi.+/
// @match        https://github.com/copilot/*
// @match        https://shareai.cfd/*
// @match        https://lmarena.ai/*
// @match        https://arena.ai/*
// @match        https://*.mjpic.cc/*
// @match        https://www.zaiwen.top/chat/*
// @match        https://chat.aite.lol/*
// @match        https://yuanbao.tencent.com/chat/*
// @match        https://chatgptup.com/*
// @match        https://ihe5u7.aitianhu2.top/*
// @match        https://cc01.plusai.io/*
// @match        https://arc.aizex.me/*
// @match        https://www.chatwb.com/*
// @match        https://www.xixichat.top/*
// @match        https://zchat.tech/*
// @match        https://*.sorryios.*/*
// @match        https://monica.im/*
// @match        https://copilot.microsoft.com/*
// @match        https://gptsdd.com/*
// @match        https://max.bpjgpt.top/*
// @match        https://nbai.tech/
// @match        https://x.liaobots.work/*
// @match        https://x.liaox.ai/*
// @match        https://chat.qwenlm.ai/*
// @match        https://lke.cloud.tencent.com/*
// @match        https://dazi.co/*
// @match        https://www.wenxiaobai.com/*
// @match        https://www.techopens.com/*
// @match        https://xiaoyi.huawei.com/*
// @match        https://chat.baidu.com/*
// @match        https://qrms.com/*
// @match        https://www.perplexity.ai/*
// @match        https://sider.ai/*
// @match        https://saas.ai1.bar/*
// @match        https://sx.xiaoai.shop/*
// @match        https://oai.liuliangbang.vip/*
// @match        https://*.dftianyi.com/*
// @match        https://notebooklm.google.com/notebook/*
// @match        https://chat.bpjgpt.top/*
// @match        https://*.plusai.io/*
// @match        https://*.plusai.me/*
// @match        https://*.yrai.cc/*
// @match        https://aistudio.xiaomimimo.com/*
// @match        https://next-three.soruxnet.com/*
// @connect      scriptcat.org
// @connect      127.0.0.1
// @connect      localhost
// @grant        GM_xmlhttpRequest
// @grant        GM_setValue
// @grant        GM_getValue
// @grant        GM_registerMenuCommand
// @grant        GM_addValueChangeListener
// @grant        GM_openInTab
// @grant        unsafeWindow
// @run-at       document-start
// ==/UserScript==

(function () {
  'use strict';

  const TAB_ID = Math.random().toString(36).substr(2, 9);
  const LOCK_KEY = 'gpt_connector_running';
  const ENDPOINT = "http://127.0.0.1:23119/zoterogpt";
  const IS_IFRAME = window.self !== window.top;

  // 🎨 日志工具
  const log = {
    info: (...msg) => console.log(`%c[INFO]`, 'color: #2196F3', ...msg),
    warn: (...msg) => console.log(`%c[WARN]`, 'color: #FF9800; font-weight: bold', ...msg),
    err: (...msg) => console.log(`%c[ERR]`, 'color: #F44336; font-weight: bold', ...msg),
    poll: (...msg) => console.log(`%c[POLL]`, 'color: #9E9E9E', ...msg),
    upd: (...msg) => console.log(`%c[SEND]`, 'color: #9C27B0; font-weight: bold', ...msg),
    dom: (...msg) => console.log(`%c[DOM]`, 'color: #E91E63; font-weight: bold', ...msg),
    ui: (...msg) => console.log(`%c[UI]`, 'color: #00BCD4; font-weight: bold', ...msg),
  };

  const getOutputText = (resp = "", think = "") => {
    let text = ""
    if (think) {
      text += ("<think>" + think)
      if (resp) { text += "</think>\n" }
    }
    text += resp
    return text
  }

  /**
   * 高性能自动检查更新 (带本地缓存，每天只查一次)
   */
  function autoCheckUpdate(force = false) {
    const updateURL = GM_info.script.updateURL || GM_info.script.downloadURL;
    const currentVersion = GM_info.script.version;

    if (!updateURL) return;

    // 1. 读取上次检查的时间戳
    const lastCheckTime = GM_getValue('last_update_check', 0);
    const now = new Date().getTime();

    // 2. 性能核心：距离上次检查不足 12 小时 (43200000 毫秒)，直接跳过，不发任何网络请求！
    if (now - lastCheckTime < 43200000 && force == false) {
      console.log("[Zotero联动] 距上次检查更新不足 12 小时，跳过网络请求，保证极速。");
      return;
    }
    notify.message({
      text: `检查更新中...`,
      type: 'waiting',
      duration: 2500
    });
    GM_xmlhttpRequest({
      method: "GET",
      url: updateURL,
      onload: async function (response) {
        if (response.status !== 200) return;

        // 请求成功，记录当前时间，接下来 12 小时内都不会再查了
        GM_setValue('last_update_check', now);

        const match = response.responseText.match(/@version\s+([\w.-]+)/);
        if (match && match[1]) {
          const latestVersion = match[1];

          const isNewer = (curr, latest) => {
            const c = curr.split('.').map(Number);
            const l = latest.split('.').map(Number);
            for (let i = 0; i < Math.max(c.length, l.length); i++) {
              if ((c[i] || 0) < (l[i] || 0)) return true;
              if ((c[i] || 0) > (l[i] || 0)) return false;
            }
            return false;
          };

          if (isNewer(currentVersion, latestVersion)) {
            await notify.message({
              text: `发现新版本 v${latestVersion}，即将打开更新页面...`,
              type: 'waiting',
              duration: 2500
            });

            if (typeof GM_openInTab !== 'undefined') {
              GM_openInTab(GM_info.script.downloadURL || updateURL, { active: true });
            }
          } else {
            await notify.message({
              text: `已经是最新版`,
              type: 'success',
              duration: 2500
            });
          }
        }
      },
      onerror: () => console.warn("[Zotero联动] 检查更新失败")
    });
  }

  // =================================================================================================
  // 1. 网络请求封装
  // =================================================================================================
  const gmRequest = (payload, timeout = 10000) => {
    let abortFn = null;
    const promise = new Promise((resolve, reject) => {
      const ts = Date.now().toString().slice(-4);
      const action = payload.action.toUpperCase();

      const req = GM_xmlhttpRequest({
        method: "POST",
        url: ENDPOINT,
        anonymous: true,
        headers: {
          "Content-Type": "application/json",
          "Accept": "application/json"
        },
        data: JSON.stringify(payload),
        timeout: timeout,
        onload: (res) => {
          if (res.status >= 200 && res.status < 300) {
            try {
              const json = JSON.parse(res.responseText);
              resolve(json);
            } catch (e) {
              log.err(`[${ts}] ${action} JSON解析失败`);
              reject(e);
            }
          } else {
            log.err(`[${ts}] ${action} HTTP ${res.status}`);
            reject(new Error(res.statusText));
          }
        },
        onerror: (e) => { reject(e); },
        ontimeout: () => {
          if (action === "POLL") resolve({});
          else reject(new Error("Timeout"));
        }
      });
      abortFn = () => {
        req.abort();
        reject(new DOMException("Aborted", "AbortError"));
      };
    });
    return { abort: abortFn, promise };
  };


  // =================================================================================================
  // 2. 站点配置 (SITES)
  // =================================================================================================
  // =================================================================================================
  // 2. 站点配置 (SITES) - 策略模式重构版
  // =================================================================================================
  const SITES = {
    // --- 1. ChatGPT (Network) --- ✅
    ChatGPT: {
      host: ['chatgpt.com'],
      input: {
        text: { selector: '#prompt-textarea', method: "paste" },
        file: { selector: "input[type=file]", method: "paste" },
        send: '[data-testid="send-button"]',
        message: '#main section',
      },
      output: {
        type: "dom",
        parser: () => {
          try {
            const lastNode = [...document.querySelectorAll("#main section")].slice(-1)[0];
            if (!lastNode) return null;
            const messages = lastNode[Object.keys(lastNode)[1]].children.props.turn.messages.filter(
              i => i.content.content_type == "text" && i.author.role == "assistant"
            )
            const text = messages.map(i => i.content.parts.join("\n")).join("\n")
              .replace(
                /\ue200[\s\S]*?\ue202\[[^\]]*?"([^"]+)"[^\]]*\]\ue201/g,
                '$1'
              )
              // 2️⃣ 删除所有残留结构
              .replace(/\ue200[\s\S]*?\ue201/g, '')
              // 3️⃣ 清理孤立 PUA 字符（极端情况）
              .replace(/[\ue200-\ue2ff]/g, '');
            const isDone = Boolean(messages.at(-1).status == "finished_successfully");
            return { text: text, isDone: isDone };
          } catch (e) { 
            console.log(e)
            return null; }
        }
      }
    },
    MirrorChatGPT: {
      // 镜像ChatGPT需要添加位置
      host: ['leopard-x.memofun.net', "98355118.4omini.xyz"],
      input: {
        text: { selector: '#prompt-textarea', method: "paste" },
        file: { selector: "input[type=file]", method: "paste" },
        send: '[data-testid="send-button"]',
        message: '#main article',
      },
      output: {
        type: "network",
        regex: /backend-api\/f\/conversation$/,
        parser: (text) => {
          let resp = "";
          for (let line of text.split("\n")) {
            if (line.startsWith('data: {"message')) {
              try {
                const data = JSON.parse(line.split("data: ")[1])
                if (data.message.content.content_type == "text") resp = data.message.content.parts[0]
              } catch { continue }
            } else if (line.startsWith("data: {")) {
              try {
                let data = JSON.parse(line.split("data: ")[1])
                if (Array.isArray(data.v)) data = data.v.find(i => i.p == "/message/content/parts/0")
                if (data && typeof (data.v) == "string") resp += data.v;
              } catch { continue }
            }
          }
          console.log(resp)
          // 本页综述了**缺氧诱导因子（HIF）在免疫与炎症中的功能**，强调其从“低氧适应因子”扩展为“免疫调控关键节点”的角色。 fileciteturn1file0
          // entity["gene","VHL","tumor suppressor gene"] + PHD系统识别 → 泛素化降解
          // return resp.replace(/\ue200.+\ue202\[[^\]]*,\s*"([^"]+)",[^\]]*\]\ue201/g, '$1')
          //   .replace(/\ue200[\s\S]*?\ue201/g, "");
          // 1️⃣ 提取 entity name
          return resp.replace(
            /\ue200[\s\S]*?\ue202\[[^\]]*?"([^"]+)"[^\]]*\]\ue201/g,
            '$1'
          )
          // 2️⃣ 删除所有残留结构
          .replace(/\ue200[\s\S]*?\ue201/g, '')
          // 3️⃣ 清理孤立 PUA 字符（极端情况）
          .replace(/[\ue200-\ue2ff]/g, '');
        }
      }
    },

    // --- 2. Kimi (Network -> 建议改DOM但此处保留Network配置) --- ✅
    Kimi: {
      host: ['kimi.moonshot.cn', 'www.kimi.com'],
      input: {
        text: { selector: '[contenteditable="true"]', method: "lexical" }, // 新版Kimi是Lexical
        file: { selector: '.chat-input-editor-container', method: "paste" },
        send: '.send-button-container',
        message: '.chat-content-item',
      },
      output: {
        type: "network",
        regex: /ChatService\/Chat/,
        parser: (text, allText) => {
          let think = "", resp = ""
          const arr = allText.split(/\x00+[^\{]+/).filter(Boolean).map(i => {
            try { return JSON.parse(i.replace(/^{{/, "{")) } catch { return {} }
          })
          for (let data of arr) {
            if (!data.mask) { continue }
            if (data.mask.startsWith("block.think")) think += data.block.think.content || ""
            else if (data.mask.startsWith("block.text")) resp += data.block.text.content || ""
          }
          return getOutputText(resp.replace(/-\| /g, "-|\n|"), think)
        }
      }
    },

    // --- 3. Tongyi (Network) --- ✅
    Tongyi: {
      host: ['www.qianwen.com'],
      input: {
        text: { selector: '[role=textbox]', method: "paste" },
        file: { selector: '[role="textbox"]', method: "paste" },
        send: '[data-icon-type="qwpcicon-sendChat"]',
        message: '.message-card-wrap.question',
      },
      output: {
        type: "network",
        regex: /qianwen.com\/api\/v2\/chat/,
        parser: (text, allText) => {
          let think = "", resp = ""
          for (let s of allText.split("\n")) {
            try {
              if (!s || !s.startsWith("data:{")) continue
              const data = JSON.parse(s.slice(5))
              const content = data.data.messages.at(-1).content
              if (!content) continue
              resp = content.replace(/^\[\(deep_think\)\]/, "")
              if (content.startsWith("[(deep_think)]")) {
                think = data.data.messages.at(-1).meta_data.multi_load[0].content.think_content
              }
            } catch (e) { }
          }
          return getOutputText(resp, think)
        }
      }
    },

    // --- 4. Claude (Network) ---
    Claude: {
      host: ['claude.ai', 'claude.ai0.cn', 'chat.kelaode.ai'],
      input: {
        text: { selector: '[contenteditable="true"]', method: "div" },
        file: { selector: "input[type=file]", method: "input" },
        send: 'button[aria-label="Send message"], button[aria-label="發送訊息"]',
        message: '[data-test-render-count]',
      },
      output: {
        type: "network",
        regex: /chat_conversations\/.+\/completion/,
        parser: (text, allText) => {
          let resp = "";
          for (let line of text.split("\n")) {
            if (line.startsWith("data: {")) {
              try {
                const data = JSON.parse(line.split("data: ")[1])
                if (data.type && data.type == "completion") resp += data.completion || ""
                else if (data.type && data.type == "content_block_delta") resp += data.delta.text || ""
              } catch { continue }
            }
          }
          return resp;
        }
      }
    },

    // --- 5. Gemini (Network) --- ✅
    Gemini: {
      host: ['gemini.google.com'],
      input: {
        text: { selector: 'rich-textarea .textarea', method: "gemini" },
        file: { selector: '.text-input-field', method: "paste", timeout: 5000 },
        send: '.send-button',
        message: 'user-query-content',
      },
      output: {
        type: "network",
        regex: /BardFrontendService\/StreamGenerate/,
        parser: (text) => {
          let think = "", resp = ""
          for (let line of text.split(/\n\d+\n/)) {
            try {
              const data = JSON.parse(line)
              if (data[0][0] == "wrb.fr") {
                const data1 = JSON.parse(data[0][2])[4][0]
                resp = data1[1][0]
                think = data1[37][0][0]
              }
            } catch { }
          }
          return getOutputText(resp.replace(/\[cite.+?\]/g, ""), think)
        }
      }
    },

    // --- 6. Poe (DOM) --- ✅
    Poe: {
      host: ['poe.com'],
      input: {
        text: { selector: 'textarea[class*=GrowingTextArea_textArea]', method: "textarea" },
        file: { selector: ".ChatDragDropTarget_dropTarget__1WrAL", method: "drag" },
        send: '[data-button-send=true]',
        message: '[class^=LeftSideMessageHeader]', // Note: check if this selector is stable for counting
      },
      output: {
        type: "dom",
        parser: () => {
          try {
            const lastNode = [...document.querySelectorAll("[class^=ChatMessage_chatMessage] [class^=Message_selectableText]")].slice(-1)[0];
            if (!lastNode) return null;
            const props = lastNode[Object.keys(lastNode)[0]].alternate.child.memoizedProps;
            const text = props.text;
            const isDone = Boolean(lastNode.closest("[class^=ChatMessagesView_messageTuple]").querySelector("[class^=ChatMessageActionBar_actionBar]"));
            return { text: text, isDone: isDone };
          } catch (e) { return null; }
        }
      }
    },

    // --- 7. Doubao (DOM) --- ✅
    Doubao: {
      host: ['www.doubao.com'],
      input: {
        text: { selector: 'textarea.semi-input-textarea', method: "textarea" },
        file: { selector: "input[type=file]", method: "input" },
        send: 'button#flow-end-msg-send',
        message: '.list_items>div',
      },
      output: {
        type: "network",
        regex: /chat\/completion/,
        parser: (text) => {
          let think = "", resp = "", isThink = false
          for (let s of text.split("\n")) {
            if (!s.startsWith("data:")) { continue }
            let data = {}
            try {
              data = JSON.parse(s.slice(6))
            } catch { continue }
            let block = data

            if (data.patch_op) {
              if (data.patch_op.find(i => i.patch_value?.content_block?.[0]?.content?.thinking_block)) {
                isThink = !isThink
                continue
              }
              block = data.patch_op.find(i => i.patch_value?.content_block?.[0]?.content?.text_block)?.patch_value?.content_block?.[0]?.content?.text_block
            }
            if (data.content) {
              if (data.content?.content_block?.[0]?.content?.thinking_block) {
                isThink = !isThink
                continue
              }
              block = data.content.content_block[0].content.text_block
            }
            // console.log({ block, data })
            if (!block || !block.text) { continue }
            if (isThink) {
              think += block.text
            } else {
              resp += block.text
            }
          }
          return getOutputText(resp, think)
        },
        parserDOM: () => {
          try {
            const divs = document.querySelectorAll('[data-testid=message_content]');
            if (divs.length === 0) return null;
            const div = divs[divs.length - 1];
            const reactKey = Object.keys(div).find(k => k.startsWith('__reactProps') || k.startsWith('__reactFiber'));
            if (!reactKey) return null;
            const fiber = div[reactKey];
            let message;
            try {
              if (fiber.pendingProps?.children?.[0]) message = fiber.pendingProps.children[0].props.message;
              if (!message && fiber.children?.[0]) message = fiber.children[0].props.message;
            } catch (e) { }
            if (!message) return null;
            const blocks = message.content_blocks_v2;
            if (!blocks) return null;
            let resp = "", think = "";
            if (blocks[0].block_type == 10040 && blocks.length >= 2) {
              think = blocks[1]?.content?.text_block?.text || "";
              if (blocks.length == 3) resp = blocks[2]?.content?.text_block?.text || "";
            } else {
              resp = blocks[0]?.content?.text_block?.text || "";
            }
            return { text: getOutputText(resp, think), isDone: message.status === 1 };
          } catch (e) { return null; }
        }
      }
    },

    // --- 8. DeepSeek (Network) --- ✅
    DeepSeek: {
      host: ['chat.deepseek.com'],
      input: {
        text: { selector: 'textarea', method: "react" },
        file: { selector: ".bf38813a", method: "drag" },
        send: '._52c986b',
        message: '._4f9bf79',
      },
      output: {
        type: "network",
        regex: /completion$/,
        parser: (text, allText) => {
          let resp = "", think = ""
          for (let line of text.split("\n")) {
            if (line.startsWith("data: {")) {
              try {
                const data = JSON.parse(line.split("data: ")[1])
                let block = {}
                if (data.v && data.v.response) {
                  block = data.v.response.fragments[0]
                } else if (Array.isArray(data.v)) {
                  block = data.v[0]
                } else if (typeof (data.v) == "string") {
                  block = {
                    content: data.v
                  }
                }
                if (block.type) {
                  window.responseType = block.type
                }
                if (!block.content) {
                  window.responseType = "system"
                }

                if (window.responseType == "RESPONSE") {
                  resp += (block.content || "")
                } else if (window.responseType == "THINK") {
                  think += (block.content || "")
                }
              } catch (e) {
                console.log(e)
              }
            }

          }
          return getOutputText(resp, think)
        }
      }
    },

    // --- 9. Yuanbao (Network) --- ✅
    Yuanbao: {
      host: ['yuanbao.tencent.com'],
      input: {
        text: { selector: '.chat-input-editor .ql-editor', method: "div" }, // Quills editor usually div
        file: { selector: ".agent-chat__input-box", method: "drag" },
        send: '.icon-send',
        message: '.agent-chat__bubble__content',
      },
      output: {
        type: "network",
        regex: /api\/chat\/.+/,
        parser: (text, allText) => {
          let think = "", resp = ""
          for (let line of text.split("\n")) {
            if (line.startsWith("data: {")) {
              try {
                const data = JSON.parse(line.split("data: ")[1])
                if (data.type == "text") resp += (data.msg || "")
                else if (data.type == "think" || data.type == "deepSearch") think += (data.contents[0].msg || "")
                else if (data.type == "replace") resp += `![](${data.replace.multimedias[0].url})\n${data.replace.multimedias[0].desc}`
              } catch (e) { }
            }
          }
          return getOutputText(resp, think)
        }
      }
    },

    // --- 10. AIStudio (Network) --- ✅
    AIStudio: {
      host: ['aistudio.google.com'],
      input: {
        text: { selector: '.text-wrapper textarea', method: "standard" },
        file: { selector: ".text-wrapper", method: "drag" },
        send: 'ms-run-button button',
        message: 'ms-chat-turn',
      },
      output: {
        type: "network",
        regex: /GenerateContent$/,
        parser: (text) => {
          let data
          if (!text) { return }
          let n = 0
          while (!data && n <= 100) {
            try {
              data = JSON.parse(text)
            } catch {
              n += 1
              text += "]"
            }
          }
          if (!data) { return "" }
          let think = "", resp = ""
          for (let i of data[0]) {
            try {
              let s = i[0][0][0][0][0][1]
              if (i[0][0][0][0][0][12]) {
                think += s
              } else {
                resp += s
              }
            } catch { }
          }
          return getOutputText(resp, think)
        }
      }
    },

    // --- 11. ChatGLM (Network) --- ✅
    ChatGLM: {
      host: ['chatglm.cn'],
      input: {
        text: { selector: '.input-box-inner textarea', method: "standard" },
        file: { selector: "input[type=file]", method: "input" },
        send: '.enter div',
        message: '.answer',
      },
      output: {
        type: "network",
        regex: /backend-api\/assistant\/stream/,
        parser: (text) => {
          let resp = ""
          for (let line of text.split("\n")) {
            if (line.startsWith("data:")) {
              try {
                const data = JSON.parse(line.split("data:")[1])
                if (data.parts && data.parts[0] && data.parts[0].content[0].type == "text") {
                  resp = data.parts[0].content[0].text
                }
              } catch { }
            }
          }
          return resp;
        }
      }
    },

    // --- 12. Yiyan (Network) --- 不打算适配
    Yiyan: {
      host: ['yiyan.baidu.com'],
      input: {
        text: { selector: '.yc-editor', method: "standard" }, // Might need textarea or div check
        file: { selector: ".UxLYHqhv", method: "drag" },
        send: '[class^=sendInner]',
        message: '[data-chat-id]',
      },
      output: {
        type: "network",
        regex: /chat\/conversation\/v2$/,
        parser: (text, allText) => {
          let think = "", resp = ""
          for (let line of allText.split(/\n+/)) {
            if (line.startsWith("data:{")) {
              try {
                const data = JSON.parse(line.split("data:")[1])
                if (data.thoughts) think += data.thoughts.replace(/<nickname-start>(.+?)<nickname-end>/, "$1") || ""
                else if (data.data) resp += data.data.content || ""
              } catch { }
            }
          }
          return getOutputText(resp, think)
        }
      }
    },

    // --- 13. Zaiwen (Network) ---
    Zaiwen: {
      host: ['www.zaiwen.top'],
      input: {
        text: { selector: 'textarea.arco-textarea', method: "standard" },
        file: { selector: ".arco-upload-draggable", method: "drag" },
        send: 'img.send',
        message: '.sessions .item',
      },
      output: {
        type: "network",
        regex: /admin\/chatbot$/,
        parser: (text) => text
      }
    },

    // --- 14. ChanlderAi (Network) ---
    ChanlderAi: {
      host: ['mychandler.bet'],
      input: {
        text: { selector: '.chandler-content_input-area', method: "standard" },
        file: { selector: "input[type=file]", method: "input" },
        send: '.send',
        message: '.chandler-ext-content_communication-group',
      },
      output: {
        type: "network",
        regex: /api\/chat\/Chat$/,
        parser: (text) => {
          let resp = ""
          for (let line of text.split("\n")) {
            if (line.startsWith("data:{")) {
              try {
                const data = JSON.parse(line.split("data:")[1])
                resp += data.delta
              } catch { }
            }
          }
          return resp
        }
      }
    },

    // --- 15. MyTan (Network) ---
    MyTan: {
      host: ['mytan.maiseed.com.cn'],
      input: {
        text: { selector: '.talk-textarea', method: "standard" },
        file: { selector: 'input[type=file]', method: "input" }, // Assumed
        send: '.send-icon',
        message: '.message-container .mytan-model-avatar',
      },
      output: {
        type: "network",
        regex: /messages$/,
        parser: (text) => {
          let resp = ""
          for (let line of text.split("\n")) {
            if (line.startsWith("data:")) {
              try {
                const data = JSON.parse(line.split("data:")[1])
                resp += data.choices[0].delta.content
              } catch { }
            }
          }
          return resp
        }
      }
    },

    // --- 16. Coze (Network) ---
    Coze: {
      host: ['coze'],
      input: {
        text: { selector: 'textarea.rc-textarea', method: "react" },
        file: { selector: "input[type=file]", method: "input" },
        send: 'button[data-testid="bot-home-chart-send-button"]',
        message: '[data-message-id]',
      },
      output: {
        type: "network",
        regex: /conversation\/chat/,
        parser: (text) => {
          let resp = ""
          for (let line of text.split("\n")) {
            if (line.startsWith("data:{")) {
              try {
                const data = JSON.parse(line.split("data:")[1])
                if (data.message.type == "answer") resp += data.message.content || ""
              } catch { }
            }
          }
          return resp
        }
      }
    },

    // --- 17. Grok (Network) --- ✅
    Grok: {
      host: ['grok.com'],
      input: {
        text: { selector: 'div[contenteditable="true"]', method: "paste" }, // Fallback to div/paste often needed
        file: { selector: "input[type=file]", method: "input" }, // Assumed
        send: 'button[type="submit"]',
        message: '[id^=response-]',
      },
      output: {
        type: "network",
        regex: /\/responses$/,
        parser: (text, allText) => {
          let resp = "", think = ""
          for (let t of allText.split("\n")) {
            try {
              let data = JSON.parse(t).result
              if (data.response) data = data.response
              if (data.isThinking) think += data.token || ""
              else resp += data.token || ""
            } catch (e) {
              // log.info(e)
            }
          }
          // console.log({resp, think})
          return getOutputText(resp, think)
        }
      }
    },

    // --- 18. Baidu Chat (Network) ---
    Baidu: {
      host: ['chat.baidu.com'],
      input: {
        text: { selector: '#chat-input-box', method: "standard" }, // innerText set
        file: { selector: "[class^=chat-bottom-wrapper]", method: "drag" },
        send: '.send-icon',
        message: '[class^=index_answer-container]',
      },
      output: {
        type: "network",
        regex: /conversation$/,
        parser: (text, allText) => {
          let resp = "", think = ""
          for (let t of allText.split("\n")) {
            if (!t.startsWith("data:")) continue
            try {
              const data = JSON.parse(t.slice(5)).data
              if (!data) continue
              if (data.message.metaData.state == "generating-resp") {
                if (data.message.content.generator.component == "reasoningContent") think += data.message.content.generator.data.value || ""
                else if (data.message.content.generator.component == "markdown-yiyan") resp += data.message.content.generator.data.value || ""
              }
            } catch { }
          }
          return getOutputText(resp, think)
        }
      }
    },

    // --- 19. Perplexity (Network) --- ✅
    Perplexity: {
      host: ['www.perplexity.ai'],
      input: {
        text: { selector: '[id=ask-input]', method: "lexical" }, // Likely lexical/paste
        file: { selector: "input[type=file]", method: "input" }, // Assumed
        send: 'button[aria-label=提交]',
        message: '.-inset-md',
      },
      output: {
        type: "network",
        regex: /perplexity_ask$/,
        parser: (text) => {
          let resp = ""
          for (let line of text.split("\n")) {
            if (line.startsWith("data:")) {
              try {
                const data = JSON.parse(line.split("data:")[1])
                if (data.blocks) {
                  for (let block of data.blocks) {
                    if (block.intended_usage == "ask_text") {
                      if (block.markdown_block && block.markdown_block.answer)
                        resp = block.markdown_block.answer || ""
                      else if (block.diff_block && block.diff_block.field == "markdown_block") {
                        for (let patch of block.diff_block.patches) {
                          if (patch.op == "replace" && patch.path == "/answer") {
                            resp = patch.value || ""
                          }
                          else if (patch.op == "add") {
                            resp += patch.value || ""
                          }
                        }
                      }
                    }
                  }
                }
              } catch (e) {
                log.err(e)
              }
            }
          }
          return resp
        }
      }
    },

    // --- 20. Sider (Network) ---
    Sider: {
      host: ['sider.ai'],
      input: {
        text: { selector: 'textarea.chatBox-input', method: "textarea" },
        file: { selector: "input[type=file]", method: "input" }, // Assumed
        send: '.send-btn',
        message: '.message-item',
      },
      output: {
        type: "network",
        regex: /(completions|chat\/wisebase)/,
        parser: (text, allText) => {
          let think = "", resp = ""
          for (let line of allText.split("\n")) {
            if (line.startsWith("data:")) {
              try {
                const data = JSON.parse(line.split("data:")[1])
                if (data.data.type == "reasoning_content") think += data.data.reasoning_content.text || ""
                else if (data.data.type == "text") resp += data.data.text || ""
              } catch { }
            }
          }
          return getOutputText(resp, think)
        }
      }
    },

    // --- 21. Qwen (Network) --- ✅
    Qwen: {
      host: ['chat.qwen.ai'],
      input: {
        text: { selector: '.message-input-container-area textarea', method: "textarea" },
        file: { selector: ".message-input-container-area", method: "drag" },
        send: 'button.send-button',
        message: '.qwen-chat-message',
      },
      output: {
        type: "network",
        regex: /chat\/completions/,
        parser: (text, allText) => {
          let think = "", resp = ""
          for (let line of allText.split("\n")) {
            if (line.startsWith("data: {")) {
              try {
                const data = JSON.parse(line.split("data:")[1])
                if (data.choices[0].delta.phase == "think") think += data.choices[0].delta.content
                else if (data.choices[0].delta.phase == "answer") resp += data.choices[0].delta.content
              } catch { }
            }
          }
          return getOutputText(resp, think)
        }
      }
    },

    // --- 22. AskManyAI (Network) --- ✅
    AskManyAI: {
      host: ['askmanyai.chat'],
      input: {
        text: { selector: '.editor', method: "paste" },
        file: { selector: "input[type=file]", method: "input" },
        send: '.fs_button',
        message: '.main-chat-view .bubble-ai',
      },
      output: {
        type: "network",
        regex: /engine\/sseQuery/,
        parser: (text, allText) => {
          let think = "", resp = ""
          for (let line of allText.split("\n")) {
            if (line.startsWith("data: {")) {
              try {
                const data = JSON.parse(line.split("data:")[1])
                if (data.content.startsWith("[HIT-REF]")) continue
                if (data.event == "thinking") think += data.content
                else if (data.event == "resp") resp += data.content
              } catch { }
            }
          }
          return getOutputText(resp, think)
        }
      }
    },

    // --- 23. Wenxiaobai (Network) --- ✅
    Wenxiaobai: {
      host: ['www.wenxiaobai.com'],
      input: {
        text: { selector: '[class^=MsgInput_input_box] textarea', method: "textarea" },
        file: { selector: "[class^=botChatPage_input_content_container]", method: "drag" },
        send: '#j-input-send-msg',
        message: '#chat_turn_container',
      },
      output: {
        type: "network",
        regex: /conversation\/chat\/v\d$/,
        parser: (text, allText) => {
          if (!allText) return ""
          let resp = ""
          for (let line of allText.replace(/event:message\ndata/g, "message").split("\n")) {
            if (line.startsWith("message:{")) {
              try {
                const data = JSON.parse(line.split("message:")[1])
                resp += data.content || ""
              } catch { }
            }
          }
          resp = resp.replace(/^```ys_think[\s\S]+?\n\n```\n/, "").replace(/[\s\S]+?```ys_think/, "```ys_think")
          if (resp.includes("```ys_think")) {
            resp = ">" + resp.split("\n").slice(3).join("\n>")
          }
          return resp
        }
      }
    },

    // --- 24. GoogleNotebookLM (Network) ---
    GoogleNotebookLM: {
      host: ['notebooklm.google.com'],
      input: {
        text: { selector: 'textarea.query-box-input', method: "standard" },
        file: { selector: "input[type=file]", method: "input" }, // Assumed
        send: 'button[type="submit"]',
        message: 'chat-message',
      },
      output: {
        type: "network",
        regex: /GenerateFreeFormStreamed/,
        parser: (text) => {
          let resp = ""
          for (let line of text.split(/\n\d+\n/)) {
            try {
              const data = JSON.parse(line)
              if (data[0][0] == "wrb.fr") {
                const data1 = JSON.parse(data[0][2])
                resp = data1[0][0]
              }
            } catch { }
          }
          return resp
        }
      }
    },

    // --- 25. MinMax (Network) --- 不太适合联动使用，不好适配
    MinMax: {
      host: ['minimaxi'],
      input: {
        text: { selector: '.chat-input-container [contenteditable]', method: "paste" },
        file: { selector: "input[type=file]", method: "input" }, // Assumed
        send: '#input-send-icon div',
        message: '.mb-4 ',
      },
      output: {
        type: "network",
        regex: /v1\/chat\/get_chat_detail/,
        parser: (text) => {
          let resp = "", think = ""
          try {
            const s = text.split("\n").find(i => i.startsWith("data:"))
            const data = JSON.parse(s.slice(5))
            const content = data.data.messageResult.content
            if (content.startsWith("<think>")) {
              if (content.includes("</think>")) {
                const res = content.match(/<think>([\s\S]*?)<\/think>([\s\S]*)/)
                think = res[1] || ""; resp = res[2] || ""
              } else {
                think = content.replace(/^<think>/, "")
              }
            } else {
              resp = content
            }
          } catch { }
          return getOutputText(resp, think)
        }
      }
    },

    // --- 26. LMArena (Network) --- ✅
    LMArena: {
      host: ['arena'],
      input: {
        text: { selector: 'form textarea', method: "textarea" },
        file: { selector: "input[type=file]", method: "input" }, // Assumed
        send: 'button[type="submit"]',
        message: 'main ol>div',
      },
      output: {
        type: "network",
        regex: /stream\/post-to-evaluation/,
        parser: (text) => {
          let res = "", think = ""
          for (let line of text.split("\n")) {
            if (line.startsWith("ag:")) think += JSON.parse(line.slice(3))
            if (line.startsWith("a0:")) res += JSON.parse(line.slice(3))
          }
          return getOutputText(res, think)
        }
      }
    },

    // --- 27. GitHubCopilot (Network) ---
    GitHubCopilot: {
      host: ['github.com'],
      input: {
        text: { selector: 'textarea#copilot-chat-textarea', method: "copilot" },
        file: { selector: "input[type=file]", method: "input" }, // Assumed
        send: '[class^=ChatInput-module__toolbarButtons] button',
        message: '.message-container',
      },
      output: {
        type: "network",
        regex: /github\/chat\/threads\/.+\/messages/,
        parser: (text) => {
          let res = ""
          for (let line of text.split("\n")) {
            if (line.startsWith("data:")) {
              const data = JSON.parse(line.slice(5))
              if (data.type == "content") res += data.body
            }
          }
          return res
        }
      }
    },

    // --- 28. MIMO (Network) --- ✅
    MIMO: {
      host: ['aistudio.xiaomimimo.com'],
      input: {
        text: { selector: 'textarea', method: "textarea" },
        file: { selector: "input[type=file]", method: "input" }, // Assumed
        send: '.dialogue-container>div:nth-child(2) button:nth-child(3)',
        message: '.markdown-prose',
      },
      output: {
        type: "network",
        regex: /open-apis\/bot\/chat/,
        parser: (text) => {
          let res = ""
          for (let line of text.split("\n")) {
            if (line.startsWith("data:")) {
              try {
                const data = JSON.parse(line.slice(5))
                if (data.type == "text") res += data.content.replace("\u0000", "") || ''
              } catch (e) {

              }
            }
          }
          return res
        }
      }
    },

    // --- 29. TencentDeepSeek (DOM) ---
    TencentDeepSeek: {
      host: ['lke.cloud.tencent.com'],
      input: {
        text: { selector: '.question-input-inner__textarea', method: "vue" },
        file: { selector: "input[type=file]", method: "input" },
        send: '.question-input', // Handled by vue method side effect or generic click
        message: '.client-chat',
      },
      output: {
        type: "dom",
        parser: () => {
          try {
            const div = document.querySelector(".client-chat");
            const msg = div.__vue__.msgList.slice(-1)[0];
            const isDone = msg.is_final;
            let text = msg.content;
            if (!text && msg.agent_thought) {
              text = "> " + msg.agent_thought.procedures[0].debugging.content.trim().replace(/\n+/g, "\n");
            }
            return { text: text, isDone: isDone };
          } catch (e) { return null; }
        }
      }
    },

    // --- 30. Xiaoyi (DOM) ---
    Xiaoyi: {
      host: ['xiaoyi.huawei.com'],
      input: {
        text: { selector: 'textarea', method: "standard" },
        file: { selector: "input[type=file]", method: "input" }, // Assumed
        send: '.send-button',
        message: '.receive-box',
      },
      output: {
        type: "dom",
        parser: () => {
          try {
            const div = [...document.querySelectorAll(".receive-box")].slice(-1)[0];
            const isDone = Boolean(div.closest(".msg-content") && div.closest(".msg-content").querySelector(".tool-bar"));
            const text = div.querySelector(".answer-cont").innerHTML;
            return { text: text, isDone: isDone };
          } catch (e) { return null; }
        }
      }
    },

    // --- 31. Copilot (DOM) ---
    Copilot: {
      host: ['copilot.microsoft.com'],
      input: {
        text: { selector: 'textarea#userInput', method: "standard" },
        file: { selector: "input[type=file]", method: "input" }, // Assumed
        send: '[data-testid="submit-button"]',
        message: '[data-content=ai-message]',
      },
      output: {
        type: "dom",
        parser: () => {
          try {
            const lastAnwser = [...document.querySelectorAll('[data-content=ai-message]')].slice(-1)[0];
            const props = lastAnwser[Object.keys(lastAnwser)[0]].pendingProps.children[1][0].props;
            return { text: props.item.text, isDone: props.isStreamingComplete };
          } catch (e) { return null; }
        }
      }
    },

    // --- 32. Microsoft (DOM - Old Style) ---
    Microsoft: {
      // NOTE: Host duplicate with Copilot, might need manual merge or strict host check
      host: ['copilot.microsoft.com'],
      input: {
        text: { selector: '[id^=chatMessageResponser]', method: "lexical" },
        file: { selector: "input[type=file]", method: "input" }, // Assumed
        send: 'button[type="submit"]',
        message: '[id^=chatMessageResponser]',
      },
      output: {
        type: "dom",
        parser: () => {
          try {
            const div = document.querySelector('[id^=chatMessageResponser]');
            const text = div[Object.keys(div)[1]].children[0].props.text;
            const isDone = div.closest('[role="article"]').querySelector(".fai-CopilotMessage__footnote");
            return { text: text, isDone: isDone };
          } catch (e) { return null; }
        }
      }
    },
    Monica: {
      // NOTE: Host duplicate with Copilot, might need manual merge or strict host check
      host: ['monica.im'],
      input: {
        text: { selector: 'textarea.ant-input', method: "textarea" },
        file: { selector: "[class^=chat-input-v2]", method: "drag" }, // Assumed
        send: () => {
          const button = document.querySelector('[class^=input-msg-btn]')
          button[Object.keys(button)[1]].onClick({ isTrusted: true, stopPropagation: () => { } })
        },
        message: '[class^=chat-items]>[class*=chat-reply]',
      },
      output: {
        type: "network",
        regex: /api.monica.im\/api\/custom_bot\/chat/,
        parser: (text) => {
          let think = "", resp = ""
          for (let line of text.split("\n")) {
            if (line.startsWith("data:")) {
              const data = JSON.parse(line.slice(5))
              if (Boolean(data.agent_status) && Boolean(data.agent_status.type == "thinking_detail_stream")) {
                think += (data.agent_status.metadata.reasoning_detail || "")
              }
              resp += data.text
            }
          }
          return getOutputText(resp, think)
        }
      }
    }
  };


  // =================================================================================================
  // 3. Network Proxy (类结构，但极速启动)
  // =================================================================================================
  class NetworkProxy {
    constructor(connector) {
      this.connector = connector;
      this.setupFetch();
      this.setupXHR();
      log.info("⚡️ NetworkProxy 已挂载 (Document Start)");
    }

    setupFetch() {
      const originalFetch = unsafeWindow.fetch;
      const self = this;

      const proxy = new Proxy(originalFetch, {
        apply: function (target, thisArg, args) {
          const fetchPromise = Reflect.apply(target, thisArg, args);

          const input = args[0];
          const urlStr = (typeof input === 'string') ? input : (input instanceof URL ? input.href : (input?.url || ''));

          // 1. 自身请求放行
          if (urlStr.includes('zoterogpt')) return fetchPromise;

          // 2. 检查配置 (此时 DOM 可能未加载，但 Config 已在 Constructor 中读取)
          const outputConfig = self.connector.config?.output;

          if (self.connector.isConnected && self.connector.isRunning && self.connector.hasLock()) {
            if (outputConfig && outputConfig.type === 'network' && outputConfig.regex && outputConfig.regex.test(urlStr)) {
              log.info(`🎯 [Fetch] 捕获流: ${urlStr}`);

              fetchPromise.then(response => {
                if (!response.ok) return;
                try {
                  const cloned = response.clone();
                  setTimeout(() => self.readStream(cloned.body), 0);
                } catch (e) { /* ignore */ }
              }).catch(() => { });
            }
          }
          return fetchPromise;
        }
      });

      // 隐形伪装
      proxy.toString = () => 'function fetch() { [native code] }';
      unsafeWindow.fetch = proxy;
    }

    async readStream(stream) {
      const reader = stream.getReader();
      const decoder = new TextDecoder();
      let allText = "";
      const outputConfig = this.connector.config.output;

      try {
        while (true) {
          const { done, value } = await reader.read();
          if (done) break;
          const chunk = decoder.decode(value, { stream: true });
          allText += chunk;

          if (outputConfig && outputConfig.parser) {
            // 解析并传输
            const parsed = outputConfig.parser(allText, allText);
            // console.log("readStream", { parsed })
            if (parsed) this.connector.onNewData(parsed, false);
          }
        }
        if (outputConfig && outputConfig.parser) {
          this.connector.onNewData(this.connector.accumulatedText, true);
        }
      } catch (e) {
        if (e?.name === "AbortError") {
          this.connector.onNewData(this.connector.accumulatedText, true);
        } else {
          console.log("readStream error", e)
        }
      }
    }

    setupXHR() {
      const originalOpen = XMLHttpRequest.prototype.open;
      const self = this;

      XMLHttpRequest.prototype.open = function (method, url) {
        const urlStr = (typeof url === 'string') ? url : (url instanceof URL ? url.href : String(url));

        if (urlStr.includes('zoterogpt')) return originalOpen.apply(this, arguments);

        const outputConfig = self.connector.config?.output;

        if (self.connector.isConnected && self.connector.isRunning && self.connector.hasLock()) {
          if (outputConfig && outputConfig.type === 'network' && outputConfig.regex && outputConfig.regex.test(urlStr)) {
            log.info(`🎯 [XHR] 捕获流: ${urlStr}`);
            this.addEventListener('readystatechange', function () {
              if ([0, 3, 4].includes(this.readyState)) {
                try {
                  if (outputConfig.parser) {
                    if ([0].includes(this.readyState)) {
                      self.connector.isDoneSignal = true
                      self.connector.performUpdate()
                    } else {
                      const parsed = outputConfig.parser(this.responseText, this.responseText);
                      // console.log("XMLHttpRequest", { parsed })
                      if (parsed) self.connector.onNewData(parsed, [0, 4].includes(this.readyState));
                    }
                  }
                } catch (e) { console.log(e) }
              }
            });
          }
        }
        return originalOpen.apply(this, arguments);
      };
      // 隐形伪装
      XMLHttpRequest.prototype.open.toString = () => 'function open() { [native code] }';
    }
  }

  // =================================================================================================
  // 4. Connector (构造函数立即初始化 Proxy)
  // =================================================================================================
  class Connector {
    constructor() {
      // 1. 获取配置 (location.host 在 document-start 阶段可用)
      this.config = this.getSiteConfig();
      if (!this.config) return;

      // 2. 🔥🔥🔥 立即初始化 NetworkProxy (关键！不等待 DOM)
      //    只要配置里要求用 network，马上挂载钩子，抢在 Kimi 之前
      if (this.config.output && this.config.output.type === 'network') {
        this.proxy = new NetworkProxy(this);
      }

      // 3. 初始化状态
      this.mySessionSecret = Math.random().toString(36).substring(2);
      this.isConnected = false;
      this.isRunning = false;
      this.currentTaskId = null;
      this.lastTaskId = null;
      this.accumulatedText = "";
      this.isDoneSignal = false;
      this.isSendingUpdate = false;
      this.hasPendingData = false;
      this.pollReq = null;
      this.pollDelayTimer = null;
      this.domWatchInterval = null;

      // 4. 延迟初始化 DOM 依赖项 (菜单、监听器、自动连接)
      //    因为此时 body 可能还不存在
      if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', () => this.initDomDependent());
      } else {
        this.initDomDependent();
      }

      // 监听卸载
      window.addEventListener('beforeunload', () => {
        this.disconnect();
      });
    }

    // DOM 准备好后才执行的逻辑
    initDomDependent() {
      this.initMenu();
      this.setupCrossTabListener();
      this.tryAutoConnect();
    }

    getSiteConfig() {
      const host = location.host;
      for (const [name, conf] of Object.entries(SITES)) {
        if (conf.host.some(h => host.includes(h))) return { name, ...conf };
      }
      return { name: "ChatGPT", ...SITES.ChatGPT };
    }

    // --- 通用工具 ---
    acquireLock() { let lockInfo = {}; try { lockInfo = JSON.parse(GM_getValue(LOCK_KEY, "{}")); } catch (e) { } if (lockInfo && lockInfo.isLocked) { return lockInfo.tabId === TAB_ID; } else { GM_setValue(LOCK_KEY, JSON.stringify({ isLocked: true, tabId: TAB_ID })); return true; } }
    forceAcquireLock() { GM_setValue(LOCK_KEY, JSON.stringify({ isLocked: true, tabId: TAB_ID })); return true; }
    releaseLock() {
      let lockInfo = {}; try {
        lockInfo = JSON.parse(GM_getValue(LOCK_KEY, "{}"));
      } catch (e) { }
      if (lockInfo.tabId === TAB_ID) {
        GM_setValue(LOCK_KEY, JSON.stringify({ isLocked: false, tabId: null }));
      }
    }
    hasLock() { let lockInfo = {}; try { lockInfo = JSON.parse(GM_getValue(LOCK_KEY, "{}")); } catch (e) { } return lockInfo.isLocked && lockInfo.tabId === TAB_ID; }
    setupCrossTabListener() { GM_addValueChangeListener(LOCK_KEY, (name, oldVal, newVal, remote) => { if (remote) { const newLock = JSON.parse(newVal); if (newLock.isLocked && newLock.tabId !== TAB_ID) { if (this.isRunning) { log.warn("被其他标签页抢占"); this.isRunning = false; this.isConnected = false; this.killPoll(); } } } }); }

    initMenu() {
      const suffix = IS_IFRAME ? ' (Frame)' : '';
      // GM_registerMenuCommand(`⭐️ 优先${suffix}`, () => { this.isRunning = true; this.forceAcquireLock(); this.handshake(); });
      GM_registerMenuCommand(`🔗 连接${suffix}`, () => {
        this.isRunning = true; this.forceAcquireLock(); this.handshake();
      });
      GM_registerMenuCommand(`🎊 断开${suffix}`, async () => {
        this.disconnect()
        notify.message({
          text: `已停止联动`,
          type: 'success',
          duration: 2000
        });
      });

      // ================= 推荐的调用方式 =================
      // 延迟 5 秒执行，确保网页核心逻辑先加载完毕，不占用前台性能
      setTimeout(autoCheckUpdate, 2e3);
      GM_registerMenuCommand(`✨ 更新`, async () => {
        await autoCheckUpdate(true)
      });
      const showNotify = GM_getValue("showNotify", true)

      GM_registerMenuCommand(showNotify ? '⚙️ 关闭弹窗' : '⚙️ 开启弹窗', function () {
        GM_setValue("showNotify", !showNotify)

        // location.reload();
      });
      GM_registerMenuCommand(`⚙️ 关于 ${GM_info.script.version}`, async () => {
        console.log(GM_info)
        const state = connector.isConnected ? "联动中" : "未联动"
        notify.message({
          text: `${GM_info.script.version} ${connector.config.name} ${state} ${GM_info.userAgentData.platform}`,
          type: 'success',
          duration: 3000
        });
      });
    }

    tryAutoConnect() {
      if (this.acquireLock()) {
        log.info("自动连接中...");
        this.isRunning = true;
        this.handshake();
      }
    }

    disconnect() {
      // 如果本来就没有运行，直接跳过
      if (!this.isRunning && !this.isConnected) {
        this.releaseLock();
        return;
      }

      log.info("执行断开清理程序...");
      this.isRunning = false;
      this.isConnected = false;

      // 1. 掐断所有正在进行的网络请求和定时器
      this.killPoll();

      // 2. 只有当前持有控制权的页面，才有资格通知 Zotero 改名字
      if (this.hasLock()) {
        // 注意：页面关闭时不能用 await，直接发出去就行 (Fire-and-forget)
        gmRequest({
          action: "connect",
          ai: "Disconnected",
          sessionSecret: "offline_" + Date.now()
        }, 2000).promise.catch(() => { }); // 捕获错误防止控制台飘红

        log.info("已向 Zotero 发送断开状态");
      }

      // 3. 释放锁，把控制权交还给大自然
      this.releaseLock();
    }

    async handshake() {
      console.log("handshake is called")
      if (!this.isRunning) { return };
      this.killPoll();
      try {
        const res = await gmRequest({
          action: "connect",
          ai: this.config.name,
          icon: document.querySelector("link[rel*=icon]")?.href || "",
          url: location.href,
          sessionSecret: this.mySessionSecret,
          version: GM_info.script.version
        }, 5000).promise;
        if (res.status === "connected") {
          this.isConnected = true;
          this.resetTaskState()
          console.log("握手成功");
          notify.message({
            text: "Zotero: 联动成功", type: "success", duration: 3e3, timeout: 200
          })
          this.start();
        }
      } catch (e) {
        console.log(e)
        notify.message({
          text: "Zotero: 联动失败，请确保Zotero打开；若已打开，请更新插件至最新版。", type: "fail", duration: 3e3, timeout: 200
        })
        log.err("握手失败");
      }
    }

    start() {
      const outputConfig = this.config.output;
      log.info(`模式启动: ${outputConfig?.type || 'unknown'}`);
      this.startPolling();
    }

    // --- DOM Watcher ---
    startDomWatcher() {
      if (this.domWatchInterval) clearInterval(this.domWatchInterval);
      const outputConfig = this.config.output;
      if (!outputConfig || outputConfig.type !== 'dom' || !outputConfig.parser) return;

      log.dom("启动 DOM 监听器");
      let lastTextLen = 0;
      let stableCycles = 0;

      this.domWatchInterval = setInterval(async () => {
        if (!this.isRunning || !this.currentTaskId) { this.stopDomWatcher(); return; }

        const result = outputConfig.parser();
        if (result && typeof result.text === 'string') {
          const currentLen = result.text.length;
          if (result.isDone) {
            if (currentLen > lastTextLen) {
              stableCycles = 0;
              this.onNewData(result.text, false);
            } else {
              stableCycles++;
              if (stableCycles >= 5) {
                this.onNewData(result.text, true);
                this.stopDomWatcher();
              } else { this.onNewData(result.text, false); }
            }
          } else {
            stableCycles = 0;
            this.onNewData(result.text, false);
          }
          lastTextLen = currentLen;
        }
      }, 200);
    }

    stopDomWatcher() {
      if (this.domWatchInterval) {
        clearInterval(this.domWatchInterval);
        this.domWatchInterval = null;
        log.dom("停止 DOM 监听器");
      }
    }

    // --- Data Transmission ---
    onNewData(text, isDone) {
      if (!this.isRunning) return;
      this.accumulatedText = text;
      if (isDone) this.isDoneSignal = true;
      this.hasPendingData = true;
      this.tryFlushData();
    }
    tryFlushData() {
      if (this.isSendingUpdate) return;
      if (!this.hasPendingData) return;

      // 🔥 2. 只要有新数据要发，立即清除冷却定时器
      if (this.pollDelayTimer) {
        clearTimeout(this.pollDelayTimer);
        this.pollDelayTimer = null;
      }

      if (this.pollReq) {
        log.warn("🔥 为发送Update，强制掐断Poll...");
        this.killPoll();
      }
      this.performUpdate();
    }
    async performUpdate() {
      const tid = this.currentTaskId || this.lastTaskId;
      if (!tid) {
        log.info("performUpdate: no tid")
        return
      };
      this.isSendingUpdate = true;
      this.hasPendingData = false;
      const textToSend = this.accumulatedText;
      const isDoneToSend = this.isDoneSignal;
      log.upd(`>>> 发送: ${textToSend.length} chars (Done: ${isDoneToSend})`);
      try {
        const { promise } = await gmRequest({ action: "update", id: tid, text: textToSend || "", isDone: isDoneToSend, sessionSecret: this.mySessionSecret }, 8000);
        await promise;
        this.lastSentText = textToSend;
        log.upd(`<<< 发送成功`);
        this.isSendingUpdate = false;
        if (isDoneToSend) {
          log.info("任务结束");
          this.resetTaskState();
          this.startPolling();
        } else {
          if (this.hasPendingData) { log.info("递归发送"); this.performUpdate(); }
          else { this.schedulePolling(); }
        }
      } catch (e) {
        log.err("发送失败，重试");
        console.log(e)
        this.isSendingUpdate = false;
        setTimeout(() => this.tryFlushData(), 500);
      }
    }

    killPoll() { if (this.pollReq) { this.pollReq.abort(); this.pollReq = null; } if (this.pollDelayTimer) { clearTimeout(this.pollDelayTimer); this.pollDelayTimer = null; } }
    schedulePolling() { if (this.pollDelayTimer) clearTimeout(this.pollDelayTimer); this.pollDelayTimer = setTimeout(() => { this.pollDelayTimer = null; if (!this.isSendingUpdate) { log.poll("冷却结束，恢复 Poll"); this.startPolling(); } }, 3000); }

    async startPolling() {
      if (this.isSendingUpdate || this.pollReq || !this.isConnected || !this.isRunning || !this.hasLock()) return;
      this.pollReq = gmRequest({ action: "poll", sessionSecret: this.mySessionSecret }, 30e3);
      try {
        const res = await this.pollReq.promise;
        this.pollReq = null;
        if (res.error === "SESSION_EXPIRED") { log.warn("Session过期"); this.isConnected = false; return; }
        if (res.task) { log.info(`收到任务: ${res.task.id}`); this.executeTask(res.task); }
        this.startPolling();
      } catch (e) {
        log.err(e)
        this.pollReq = null;
        if (e && e.name === "AbortError") return;
        if (this.isSendingUpdate) return;
        if (this.isConnected && this.isRunning) setTimeout(() => this.startPolling(), 1000);
      }
    }

    resetTaskState() {
      this.currentTaskId = null;
      this.isDoneSignal = false;
      this.accumulatedText = "";
      this.lastSentText = "";
      this.hasPendingData = false;
      this.stopDomWatcher();
    }

    // --- Task Execution ---
    async executeTask(task) {
      try {
        log.info(`执行任务: ${task.id}`);
        console.log(task)
        this.killPoll(); // 立即静默
        this.isSendingUpdate = true;
        this.currentTaskId = task.id;
        this.lastTaskId = task.id;
        this.resetTaskState();
        this.currentTaskId = task.id;
        console.log(task.messages)
        if (task.messages && this.config.input.file) {
          for (let message of task.messages) {
            if (message.type == "file") {
              await this.uploadFile(message.base64String, message.name);
              await this.sleep(1000);
            }
          }
        }

        const prompt = task.messages.filter(m => m.type !== "file").map(m => m.text).join("\n\n");
        if (prompt) {
          const inputConfig = this.config.input.text; // 使用 input.text 配置

          let success = await this.fillInput(inputConfig, prompt);
          if (!success) { log.warn("重试填充..."); success = await this.fillInput(inputConfig, prompt); }

          if (success) {
            log.ui("输入完成，发送...");
            const sent = await this.handleSend(this.config.input.send, this.config.input.message);

            if (sent) {
              log.ui("已发送");
              if (this.config.output && this.config.output.type === 'dom') {
                this.startDomWatcher();
              }
              this.isSendingUpdate = false;
            } else {
              log.err("发送失败");
              this.isSendingUpdate = false;
              this.schedulePolling();
            }
          } else {
            log.err("填充失败");
            this.isSendingUpdate = false;
            this.schedulePolling();
          }
        } else {
          log.info("<prompt is empty>")
          this.isSendingUpdate = false;
          this.schedulePolling();
        }
      } catch (e) {
        log.err(e)
      }
    }

    // --- Input Strategies ---
    async fillInput(inputConfig, text) {
      log.info("fillInput is called")
      if (!inputConfig) return false;
      const { selector, method } = inputConfig;
      const el = document.querySelector(selector);
      if (!el) { log.err(`输入框未找到: ${selector}`); return false; }
      el.focus();

      try {
        switch (method) {
          case 'react': await this.setInputReact(el, text); break;
          case 'lexical': await this.setInputPaste(el, text); break;
          case 'div': el.innerHTML = text.split("\n").map(i => `<p>${this.escapeHtml(i)}</p>`).join(""); el.dispatchEvent(new InputEvent('input', { bubbles: true })); break;
          case 'paste': await this.setInputPaste(el, text); break;
          case 'gemini': el.textContent = text; el.dispatchEvent(new InputEvent('input', { bubbles: true })); break;
          case 'textarea': await this.setInputTextarea(el, text); break;
          case 'vue': await this.setInputVue(el, text); break;
          case 'standard': default: await this.setInputStandard(el, text); break;
        }
        await this.sleep(100);
        el.dispatchEvent(new Event('input', { bubbles: true }));
        return true;
      } catch (e) { log.err(`填充错误 ${method}`, e); return false; }
    }

    // Input Helpers
    escapeHtml(str) { return str.replace(/[&<>"']/g, m => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' })[m]); }

    async setInputStandard(el, text) {
      // 获取 input 输入框的dom对象
      var inputNode = el
      if (!inputNode) { return }
      inputNode.value = text;
      // plus
      try {
        inputNode.innerHTML = text.split("\n").map(i => `<p>${escapeHtml(i)}</p>`).join("\n");
      } catch { }
      // 设置输入框的 input 事件
      var event = new InputEvent('input', {
        'bubbles': true,
        'cancelable': true,
      });
      inputNode.dispatchEvent(event);
    }

    async setInputTextarea(el, text) {
      const textarea = el
      const props = Object.values(textarea)[1]

      // 获取目标 DOM 节点（假设 temp2 是 DOM 元素引用）
      const targetElement = textarea;

      // 创建伪事件对象
      const e = {
        target: targetElement,
        currentTarget: targetElement,
        type: 'change',
      };

      // 手动设置值（需同时更新 DOM 和 React 状态）
      targetElement.value = text;

      // 触发 React 的 onChange 处理
      await props.onChange(e);
    }

    async setInputReact(el, text) {
      const key = Object.keys(el).find(k => k.startsWith('__reactProps'));
      if (key) {
        const props = el[key];
        // Try standard onChange or value tracker
        if (props.onChange) {
          props.onChange({ target: { value: text }, currentTarget: { value: text } });
        }
        // Fallback for some Ant Design or specific wrappers (like Monica)
        if (props.children && props.children.props && props.children.props.onChange) {
          props.children.props.onChange({ target: { value: text } });
        }
      } else {
        // Fallback to standard if React props not found
        await this.setInputStandard(el, text);
      }
    }

    async setInputPaste(el, text) { const dt = new DataTransfer(); dt.setData('text/plain', text); el.dispatchEvent(new ClipboardEvent('paste', { bubbles: true, cancelable: true, clipboardData: dt })); }
    async setInputVue(el, text) { try { document.querySelector(".question-input")?.__vue__?.onStopStream(); if (el.__vue__?.onChange) await el.__vue__.onChange(text.slice(0, 10000)); } catch (e) { } }


    async handleSend(send, messageSelector, retry = 0) {
      let sendFunction = null;
      if (typeof (send) == "function") {
        sendFunction = send;
      } else {
        sendFunction = () => {
          log.info(`点击 ${send}`);
          const btn = document.querySelector(send);
          if (btn) {
            btn.click();
            btn.dispatchEvent(new MouseEvent('mousedown', { bubbles: true }));
            btn.dispatchEvent(new MouseEvent('mouseup', { bubbles: true }));
          }
        }
      }

      this.killPoll();
      this.isSendingUpdate = true;

      // --- 获取当前状态 ---
      const getMessages = () => document.querySelectorAll(messageSelector);
      const lastMsgAtStart = getMessages()[getMessages().length - 1];

      // 记录初始特征：要么是元素的引用，要么是内容，或者 null
      const initialContent = lastMsgAtStart ? lastMsgAtStart.innerText : null;
      const initialCount = getMessages().length;

      log.ui(`准备发送，初始消息数: ${initialCount}`);

      sendFunction();
      const maxRetries = 30;
      for (let i = 0; i < maxRetries; i++) {
        const currentMessages = getMessages();
        const currentCount = currentMessages.length;
        const currentLastMsg = currentMessages[currentCount - 1];

        // --- 判定逻辑更新 ---
        let isSuccess = false;

        if (initialCount === 0) {
          // 场景 A: 初始没有消息 -> 只要现在有了，就算成功
          if (currentCount > 0) isSuccess = true;
        } else {
          // 场景 B: 初始已有消息
          // 1. 数量增加了
          if (currentCount > initialCount) isSuccess = true;
          // 2. 数量没变，但最后一个元素变了（比如 React/Vue 重新渲染了节点）
          else if (currentLastMsg !== lastMsgAtStart) isSuccess = true;
          // 3. 元素还是那个，但内容变了（比如从“输入中...”变成了实际内容）
          else if (currentLastMsg && currentLastMsg.innerText !== initialContent) isSuccess = true;
        }

        if (isSuccess) {
          log.ui(`发送成功：检测到末尾状态变化 (${initialCount} -> ${currentCount})`);
          this.isSendingUpdate = false;
          this.schedulePolling();
          return true;
        }
        await this.sleep(100);
      }
      if (retry < 10) {
        log.err("3 秒内未产生变化, 重新发送...");
        return await this.handleSend(send, messageSelector, retry + 1)
      }
      log.err("发送失败：末尾元素在 3 秒内未产生变化");
      this.isSendingUpdate = false;
      this.schedulePolling();
      return false;
    }

    async uploadFile(base64String, fileName) {
      try {
        const fileConfig = this.config.input.file || { method: "input", selector: "input[type=file]" };
        console.log(fileConfig)
        const { method, selector, timeout } = fileConfig;
        const fileType = this.getFileType(fileName);
        const fileContent = this.base64ToArrayBuffer(base64String);
        const file = new File([fileContent], fileName, { type: fileType });
        log.info(`上传文件: ${fileName} (${method})`);
        if (method === "input") {
          const dataTransfer = new DataTransfer();
          dataTransfer.items.add(file);
          let fileInput;
          const fileInputs = document.querySelectorAll(selector);
          if (fileInputs.length === 1) fileInput = fileInputs[0];
          else fileInput = [...fileInputs].find(i => i.accept.includes(fileType) || i.multiple) || fileInputs[0];
          if (fileInput) {
            fileInput.files = dataTransfer.files;
            fileInput.dispatchEvent(new Event('change', { bubbles: true }));
          }
        } else if (method === "drag") {
          const dataTransfer = new DataTransfer();
          dataTransfer.items.add(file);

          const dropZone = document.querySelector(selector); // 使用提供的选择器查找拖放区域
          const dragStartEvent = new DragEvent("dragstart", {
            bubbles: true,
            dataTransfer: dataTransfer,
            cancelable: true
          });
          const dropEvent = new DragEvent("drop", {
            bubbles: true,
            dataTransfer: dataTransfer,
            cancelable: true
          });

          dropZone.dispatchEvent(dragStartEvent);
          dropZone.dispatchEvent(dropEvent);
        } else if (method === "paste") {
          const dt = new DataTransfer();
          dt.items.add(file);
          const pasteEvent = new ClipboardEvent("paste", { bubbles: true, cancelable: true });
          Object.defineProperty(pasteEvent, "clipboardData", { value: dt });
          const target = document.querySelector(selector);
          if (target) { target.focus(); target.dispatchEvent(pasteEvent); }
        }
        if (timeout) await this.sleep(timeout);
      } catch (e) { log.err("文件上传失败", e); }
    }

    sleep(ms) { return new Promise(r => setTimeout(r, ms)); }

    getFileType(fileName) {
      if (fileName.endsWith("pdf")) return "application/pdf";
      if (fileName.endsWith("png")) return "image/png";
      if (fileName.endsWith("jpg") || fileName.endsWith("jpeg")) return "image/jpeg";
      if (fileName.endsWith("txt") || fileName.endsWith("md")) return "text/plain";
      if (fileName.endsWith("html")) return "text/html";
      return "application/octet-stream";
    }

    base64ToArrayBuffer(base64) {
      const binaryString = window.atob(base64);
      const len = binaryString.length;
      const bytes = new Uint8Array(len);
      for (let i = 0; i < len; i++) { bytes[i] = binaryString.charCodeAt(i); }
      return bytes.buffer;
    }
  }

  class NoticeManager {
    constructor() {
      if (GM_getValue("showNotify", true) == false) { return }
      this.overlay = null;
      this.box = null;
      this.contentWrap = null;

      this.itv = null;
      this.closeTimer = null;
      this.resolveActive = null;

      this._injectStyle();
    }

    // ================= 1. 纯净 DOM 构建引擎 (免疫一切拦截) =================
    _el(tag, attrs = {}, children = []) {
      // 自动识别 SVG 标签，使用正确的命名空间创建
      const isSvg = ['svg', 'path', 'polyline', 'circle', 'line'].includes(tag);
      const el = isSvg
        ? document.createElementNS('http://www.w3.org/2000/svg', tag)
        : document.createElement(tag);

      for (const [key, value] of Object.entries(attrs)) {
        if (key === 'className') el.setAttribute('class', value);
        else if (key === 'style') el.style.cssText = value;
        else el.setAttribute(key, value);
      }

      const kids = Array.isArray(children) ? children : [children];
      for (const child of kids) {
        if (typeof child === 'string') el.appendChild(document.createTextNode(child));
        else if (child instanceof Node) el.appendChild(child);
      }
      return el;
    }

    // ================= 2. 注入 CSS (使用文本节点，告别 innerHTML) =================
    _injectStyle() {
      const styleId = 'custom-confirm-style';
      if (document.getElementById(styleId)) return;

      const style = document.createElement('style');
      style.id = styleId;
      const cssText = `
            .conf-overlay { position: fixed; top: 20px; left: 50%; transform: translateX(-50%); z-index: 2147483647; pointer-events: none; }
            .conf-box { pointer-events: auto; background: #fff; padding: 8px 16px; border-radius: 50px; display: flex; align-items: center; justify-content: center; box-shadow: 0 8px 24px rgba(0, 0, 0, 0.12); border: 1px solid rgba(0, 0, 0, 0.06); animation: slideInTop 0.5s cubic-bezier(0.175, 0.885, 0.32, 1.15) forwards; transition: width 0.35s cubic-bezier(0.4, 0, 0.2, 1); box-sizing: border-box; overflow: hidden; white-space: nowrap; }
            .conf-box.exit { animation: slideOutTop 0.4s cubic-bezier(0.6, -0.28, 0.735, 0.045) forwards; }
            @keyframes slideInTop { from { transform: translateY(-100px); opacity: 0; } to { transform: translateY(0); opacity: 1; } }
            @keyframes slideOutTop { from { transform: translateY(0); opacity: 1; } to { transform: translateY(-100px); opacity: 0; } }
            @keyframes fadeIn { from { opacity: 0; transform: scale(0.95); } to { opacity: 1; transform: scale(1); } }
            .conf-content { display: flex; align-items: center; gap: 14px; width: max-content; }
            .conf-text { color: #1f2937; font-size: 14px; font-weight: 500; }
            .conf-btns { display: flex; gap: 8px; align-items: center; }
            .conf-btn { cursor: pointer; border: none; height: 32px; border-radius: 16px; display: flex; align-items: center; justify-content: center; transition: all 0.2s; font-size: 13px; font-weight: 500; gap: 4px; }
            .conf-cancel { background: #f3f4f6; color: #4b5563; padding: 0 14px; }
            .conf-cancel:hover { background: #e5e7eb; color: #111827; }
            .conf-ok { background: #ef4444; color: #fff; padding: 0 14px; }
            .conf-ok:hover { background: #dc2626; transform: scale(1.02); box-shadow: 0 4px 10px rgba(239, 68, 68, 0.3); }
            .t-val { font-size: 11px; opacity: 0.8; margin-left: 2px; }
        `;
      style.appendChild(document.createTextNode(cssText));
      document.head.appendChild(style);
    }

    _clearState() {
      clearInterval(this.itv);
      clearTimeout(this.closeTimer);
      if (this.resolveActive) {
        this.resolveActive(false);
        this.resolveActive = null;
      }
    }

    // ================= 3. 核心：处理 DOM 复用与宽度过渡动画 =================
    // 此时接收的是原生 Node 节点，而非 HTML 字符串
    _renderContent(nodeMap) {
      if (!this.overlay || !document.body.contains(this.overlay)) {
        this.contentWrap = this._el('div', { className: 'conf-content' }, [nodeMap]);
        this.box = this._el('div', { className: 'conf-box' }, [this.contentWrap]);
        this.overlay = this._el('div', { className: 'conf-overlay' }, [this.box]);
        document.body.appendChild(this.overlay);
      } else {
        this.box.classList.remove('exit');

        const oldWidth = this.box.offsetWidth;
        this.box.style.width = oldWidth + 'px';

        // 安全清空旧节点，追加新节点
        while (this.contentWrap.firstChild) this.contentWrap.removeChild(this.contentWrap.firstChild);
        this.contentWrap.appendChild(nodeMap);

        this.box.style.width = 'auto';
        const newWidth = this.box.offsetWidth;

        this.box.style.width = oldWidth + 'px';
        this.box.offsetHeight; // 强制重绘
        this.box.style.width = newWidth + 'px';

        setTimeout(() => { if (this.box) this.box.style.width = 'auto'; }, 350);
      }
    }

    close() {
      if (this.overlay && this.box) {
        this.box.classList.add('exit');
        setTimeout(() => {
          if (this.overlay && this.overlay.parentNode) {
            this.overlay.parentNode.removeChild(this.overlay);
          }
          this.overlay = null;
        }, 400);
      }
    }

    // ================= 4. 公开方法 =================
    message(options = {}) {
      if (GM_getValue("showNotify", true) == false) { return }
      this._clearState();
      console.log("message", options);

      return new Promise(resolve => {
        const { text = "操作成功", type = "success", duration = 1500, timeout = 0 } = options;

        // 根据状态构建你自定义的 SVG 图标
        let svgNode;
        if (type === 'success') {
          svgNode = this._el('svg', { width: "20", height: "20", viewBox: "0 0 24 24", fill: "none", stroke: "#10b981", "stroke-width": "2.5", "stroke-linecap": "round", "stroke-linejoin": "round" }, [
            this._el('polyline', { points: "20 6 9 17 4 12" })
          ]);
        } else if (type === "fail" || type === "cancel") {
          svgNode = this._el('svg', { width: "20", height: "20", viewBox: "0 0 24 24", fill: "none", stroke: "#ef4444", "stroke-width": "2.5", "stroke-linecap": "round", "stroke-linejoin": "round" }, [
            this._el('circle', { cx: "12", cy: "12", r: "10" }),
            this._el('line', { x1: "15", y1: "9", x2: "9", y2: "15" }),
            this._el('line', { x1: "9", y1: "9", x2: "15", y2: "15" })
          ]);
        } else if (type === 'ok' || type === 'timeout' || type === 'waiting') {
          // 等待 / 超时 (你的灰色向日葵/时钟图标)
          svgNode = this._el('svg', { viewBox: "0 0 1024 1024", width: "20", height: "20" }, [
            this._el('path', { fill: "#666666", d: "M329.3 513.2c0-20-16.2-36.2-36.2-36.2H121.6c-20 0-36.2 16.2-36.2 36.2 0 20 16.2 36.2 36.2 36.2h171.5c20 0 36.2-16.2 36.2-36.2zM902.4 477H730.9c-20 0-36.2 16.2-36.2 36.2 0 20 16.2 36.2 36.2 36.2h171.5c20 0 36.2-16.2 36.2-36.2 0.1-20-16.2-36.2-36.2-36.2zM512.4 706.4c-20 0-36.2 16.2-36.2 36.2V902c0 20 16.2 36.2 36.2 36.2 20 0 36.2-16.2 36.2-36.2V742.7c0-20-16.2-36.3-36.2-36.3zM512.4 85.7c-20 0-36.2 16.2-36.2 36.2v171.5c0 20 16.2 36.2 36.2 36.2 20 0 36.2-16.2 36.2-36.2V121.9c0-20-16.2-36.2-36.2-36.2zM330.8 640.6L209.6 761.8c-14.1 14.1-14.1 37.1 0 51.2 7.1 7.1 16.3 10.6 25.6 10.6s18.5-3.5 25.6-10.6l121.3-121.3c14.1-14.1 14.1-37.1 0-51.2-14.2-14.1-37.1-14.1-51.3 0.1zM665.4 393.4c9.3 0 18.5-3.5 25.6-10.6l121.3-121.3c14.1-14.1 14.1-37.1 0-51.2-14.1-14.1-37.1-14.1-51.2 0L639.8 331.5c-14.1 14.1-14.1 37.1 0 51.2 7.1 7.1 16.3 10.7 25.6 10.7zM700.5 649c-14.1-14.1-37.1-14.1-51.2 0-14.1 14.1-14.1 37.1 0 51.2L762 813c7.1 7.1 16.3 10.6 25.6 10.6s18.5-3.5 25.6-10.6c14.1-14.1 14.1-37.1 0-51.2L700.5 649zM260.8 211.3c-14.1-14.1-37.1-14.1-51.2 0-14.1 14.1-14.1 37.1 0 51.2l121.3 121.3c7.1 7.1 16.3 10.6 25.6 10.6s18.5-3.5 25.6-10.6c14.1-14.1 14.1-37.1 0-51.2L260.8 211.3z" })
          ]);
        }

        // 构建 DOM: <div> <svg>...</svg> <span>text</span> </div>
        const contentNode = this._el('div', { style: "display:flex; align-items:center; gap:8px; animation: fadeIn 0.3s ease forwards; padding: 2px 6px;" }, [
          svgNode,
          this._el('span', { style: "color:#374151; font-size:15px; font-weight:600;" }, text)
        ]);

        setTimeout(() => {
          this._renderContent(contentNode);
          this.closeTimer = setTimeout(() => {
            this.close();
            resolve(true);
          }, duration);
        }, timeout);
      });
    }

    confirm(options = {}) {
      if (GM_getValue("showNotify", true) == false) { return }
      this._clearState();

      return new Promise(resolve => {
        this.resolveActive = resolve;

        const {
          text = "确认执行此操作？",
          okBtnText = "确认",
          cancelBtnText = "取消",
          msgOk = "操作成功",
          msgCancel = "已取消操作",
          msgTimeout = "已自动确认",
          timeout = 5
        } = options;

        // 取消按钮
        const btnCancel = this._el('button', { className: 'conf-btn conf-cancel' }, cancelBtnText);

        // 确认按钮 (包含 SVG 和倒计时)
        const timerTextNode = document.createTextNode(`${timeout}s`);
        const timerSpan = this._el('span', { className: 't-val' }, timerTextNode);
        const okSvg = this._el('svg', { width: "14", height: "14", viewBox: "0 0 1024 1024" }, [
          this._el('path', { fill: "currentColor", d: "M939.36 218.912a32 32 0 0 1 45.856 44.672l-538.016 552a32 32 0 0 1-43.776 1.92L63.872 526.048a32 32 0 1 1 41.696-48.544l316.768 271.936L939.36 218.88z" })
        ]);
        const btnOk = this._el('button', { className: 'conf-btn conf-ok' }, [okSvg, " " + okBtnText + " ", timerSpan]);

        // 组装整体布局
        const layoutNode = this._el('div', { style: 'display:flex; align-items:center; gap:14px;' }, [
          this._el('div', { className: 'conf-text' }, text),
          this._el('div', { className: 'conf-btns' }, [btnCancel, btnOk])
        ]);

        this._renderContent(layoutNode);

        let timeLeft = timeout;

        const handleResult = (type) => {
          clearInterval(this.itv);
          this.resolveActive = null;

          let isSuccess = false;
          let resultMsg = "";

          if (type === 'ok') { resultMsg = msgOk; isSuccess = true; }
          else if (type === 'cancel') { resultMsg = msgCancel; isSuccess = false; }
          else if (type === 'timeout') { resultMsg = msgTimeout; isSuccess = true; }

          // 将原状态直接传递给 message 方法
          resolve(isSuccess)
          this.message({ text: resultMsg, type: type, duration: 1.5e3, timeout: 0 })
        };

        this.itv = setInterval(() => {
          timeLeft--;
          if (timeLeft <= 0) {
            handleResult('timeout');
          } else {
            timerTextNode.nodeValue = `${timeLeft}s`;
          }
        }, 1000);

        btnOk.onclick = () => handleResult('ok');
        btnCancel.onclick = () => handleResult('cancel');
      });
    }
  }

  // 导出单例，确保全局共用同一个弹窗实例
  const notify = new NoticeManager();

  const connector = new Connector();

  document.addEventListener("DOMContentLoaded", async () => {

    // 假设 connector 对象存在
    if (!(await connector.acquireLock())) {
      const result = await notify.confirm({
        text: `Connector: 是否连接到 ${connector.config.name}`,
        okBtnText: "连接",
        cancelBtnText: "暂不",
        msgOk: "连接中...",
        msgCancel: "未连接",
        msgTimeout: "自动连接中...",
        timeout: 5
      });
      if (result) {
        console.log("执行联动操作...");
        connector.forceAcquireLock();
        connector.isRunning = true;
        await connector.handshake();
      }
    }
  })
})();

```