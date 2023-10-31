from django.shortcuts import get_object_or_404, render
from django.views.generic.base import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from FactorApp.models import User, Post, Follow, Following


class MainView(LoginRequiredMixin, TemplateView):
	template_name = 'homePage.html'

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		posts = Post.objects.all().order_by('-created_date')
		context.update({
			"posts": posts,
		})
		return context


class ProfileView(LoginRequiredMixin, TemplateView):
	template_name = 'profile.html'	

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		Years = self.request.user.dob.year
		Months = self.request.user.dob.month
		Days = self.request.user.dob.day
		user_followers = Follow.objects.get(user=self.request.user)
		user_followings = Following.objects.get(user=self.request.user)
		context.update({
			"posts": Post.objects.filter(user__email=self.request.user.email).order_by('-created_date'),
			"Gender": ['Male','Female'],
			"Year": f'{Years}',
			"Month": f'0{Months}' if Months < 10 else f'{Months}',
			"Day": f'0{Days}' if Days < 10 else f'{Days}',
			'followers': user_followers.followers.all(),
			'num_followers': user_followers.followers.count(),
			'followings': user_followings.followings.all(),
			'num_followings': user_followings.followings.count(),
		})
		return context


class OtherProfileView(LoginRequiredMixin, TemplateView):
	template_name = 'otherprofile.html'

	def get_is_following(self, obj):
		login_user = self.request.user
		followers_obj = obj.followers.all()
		has_followed = False

		if login_user in followers_obj:
			has_followed = True

		return has_followed

	def get_queryset(self):
		queryset = get_object_or_404(User, email=self.kwargs['email'])
		return queryset

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		user_followers = Follow.objects.get(user__email=self.kwargs['email'])
		user_followings = Following.objects.get(user__email=self.kwargs['email'])
			
		context.update({
			"posts": Post.objects.filter(user__email=self.kwargs['email']).order_by('-created_date'),
			'clicked_user': self.get_queryset,
			'followers': user_followers.followers.all(),
			'num_followers': user_followers.followers.count(),
			'followings': user_followings.followings.all(),
			'num_followings': user_followings.followings.count(),			
			'is_followed': self.get_is_following(user_followers)
		})
		return context