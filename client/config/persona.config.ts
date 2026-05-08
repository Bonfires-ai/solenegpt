export const personaConfig = {
  // App identity
  appName: 'Solène',
  tagline: 'Dev3pack Mentor',
  description: 'Talk to Solène Daviaud, founder of Dev3pack, about your Web3 + AI project.',
  siteUrl: 'https://dev3pack.xyz',
  blogUrl: 'https://dev3pack.xyz',

  // OG / SEO
  ogImagePath: '/og-image-1.1.png',
  favicon: {
    svg: '/favicon_io/favicon.svg',
    ico: '/favicon_io/favicon.ico',
    apple: '/favicon_io/apple-touch-icon.png',
  },

  // Landing page
  heroTitle: 'Solène',
  heroSubtitle: 'Dev3pack Mentor',
  heroDescription: 'Talk to Solène about your project. Pick English or Français and go.',
  heroAvatarImage: '/avatars/solene-en.gif',
  heroAvatarAlt: 'Solène Avatar',
  startChatButtonLabel: 'TALK WITH SOLÈNE',

  // Footer
  footer: {
    credit: 'Dev3pack',
    creditUrl: 'https://dev3pack.xyz',
    socialLinks: [
      { label: 'Dev3pack', url: 'https://dev3pack.xyz' },
      { label: 'LinkedIn', url: 'https://fr.linkedin.com/in/solene-daviaud/en' },
    ],
    githubRepo: 'https://github.com/Bonfires-ai/solenegpt',
  },

  // Moods / personas — repurposed as language selectors (same warm Solène persona)
  moods: {
    english: {
      label: 'English',
      subtitle: 'Chat with Solène in English.',
      description: 'Solène, founder of Dev3pack, ready to talk through your project — in English.',
      avatarImage: '/avatars/solene-en.gif',
      accentClass: 'bg-synthesis text-white',
      visualizerVariant: 'synthesis' as const,
      visualizerBgColor: '#A15EED',
      connectingLabel: 'Solène (English)',
    },
    french: {
      label: 'Français',
      subtitle: 'Discutez avec Solène en français.',
      description: 'Solène, fondatrice de Dev3pack, prête à parler de ton projet — en français.',
      avatarImage: '/avatars/solene-fr.gif',
      accentClass: 'bg-synthesis-dark text-white',
      visualizerVariant: 'synthesis' as const,
      visualizerBgColor: '#7C3AED',
      connectingLabel: 'Solène (Français)',
    },
  },

  // Social share copy templates
  shareCopies: [
    `Just had a 5-minute mentor session with Solène at @dev3pack.\n\n"What's the smallest version you could ship this week?"\n\nFair point.\n\nTry it → dev3pack.xyz`,
    `Solène asked me what I'd build first if I had to ship by Sunday.\n\nGreat question.\n\nGo talk to her: dev3pack.xyz\n@dev3pack`,
    `Pitched my Web3 + AI idea to Solène (Dev3pack founder, AI version).\n\nWalked away with a clearer next step than I had going in.\n\ndev3pack.xyz\n@dev3pack`,
    `Like having a Dev3pack mentor on demand.\n\nWarm. Practical. Actually useful.\n\nGo vibe → dev3pack.xyz\n@dev3pack`,
    `Talked to Solène about my project.\n\nNow I have to actually build it.\n\nIf you need builder feedback, try it → dev3pack.xyz\n@dev3pack`,
  ],

  shareCopiesWithZora: [
    `Ran my idea through Solène (@dev3pack, AI version).\nCame out with a plan to build.\n\nMinted this for the record → {{zora_link}}\n\ndev3pack.xyz`,
    `Talked to Solène at Dev3pack.\nKept the receipts.\n\nMinted → {{zora_link}}\n\ndev3pack.xyz`,
    `Solène said "just build it."\nSo I'm minting the proof.\n\n→ {{zora_link}}\n\ndev3pack.xyz`,
  ],

  // Wallet metadata (only used if Zora minting / wallet flows are enabled)
  walletMetadata: {
    name: 'Solène (Dev3pack)',
    description: 'Talk to Solène Daviaud, founder of Dev3pack',
    url: 'https://dev3pack.xyz',
    icons: ['https://avatars.githubusercontent.com/u/2653167'],
  },

  // Share frame
  shareFrame: {
    prompt: '> dev3pack_',
    excitedAvatarImage: '/frame/austin-t-excited.png',
    criticalAvatarImage: '/frame/austin-t-critical.png',
  },
};

export type PersonaConfig = typeof personaConfig;
export type MoodKey = keyof typeof personaConfig.moods;

export const isZoraMintingEnabled = process.env.NEXT_PUBLIC_ENABLE_ZORA_MINTING !== 'false';
