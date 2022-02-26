import { defineStore } from 'pinia'

export const useChatMessageStore = defineStore('chatmessage',{
    state: () => {
        return {
            msg_list: []
        }
    },
    getters: {
        receivedMessages(state) {
            return state.msg_list
        }
    },
    actions: {
        addMessage(msg) {
            this.msg_list.push(msg);
        }
    }
})