import { create } from 'zustand'
import { persist } from 'zustand/middleware'

interface TwitterAccount {
  id: string
  username: string
  isActive: boolean
}

interface AppState {
  accounts: TwitterAccount[]
  addAccount: (account: TwitterAccount) => void
  removeAccount: (accountId: string) => void
  selectedAccountId: string | null
  selectAccount: (accountId: string) => void
}

export const useAppStore = create<AppState>()(
  persist(
    (set) => ({
      accounts: [],
      selectedAccountId: null,
      addAccount: (account) => set((state) => ({
        accounts: [...state.accounts, account]
      })),
      removeAccount: (accountId) => set((state) => ({
        accounts: state.accounts.filter(account => account.id !== accountId)
      })),
      selectAccount: (accountId) => set({ selectedAccountId: accountId })
    }),
    {
      name: 'x-twitter-bot-storage',
      version: 1
    }
  )
)
