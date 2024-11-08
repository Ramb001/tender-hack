import { LucideIcon, TwitterIcon, Facebook, Instagram } from 'lucide-react';
import { ReactElement } from 'react'
import { SVGProps } from 'react';

interface FooterTypes {
	href: string;
	value?: string;
	icon?: (props: SVGProps<SVGSVGElement>) => JSX.Element;
}

export const FooterNavLinks: FooterTypes[] = [
	{
		href: '/privacy',
		value: 'Privacy Policy',
	},
	{
		href: '/terms',
		value: 'Terms of Service',
	},
]

export const FooterSocialLinks: FooterTypes[] = [
	{
		href: 'https://twitter.com',
		icon: TwitterIcon,
	},
	{
		href: 'https://facebook.com',
		icon: Facebook
	},{
		href: 'https://instagram.com',
		icon: Instagram
	},
]